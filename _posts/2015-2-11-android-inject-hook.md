---
date: 2015-2-11 11:11:30+00:00
layout: post
title: Android下的挂钩(hook)和代码注入(inject)
thread: 97
categories: cocos2d-x android
tags: cocos2d-x android
---

Android是基于linux内核的操作系统，根据语言环境可以简单的划分为java层、native C层、linux内核层。java层通过jni与native层交互，使用linux提供的底层函数功能。

因此，类似linux系统，我们可以在Android下实现对另一个进程的挂钩和代码注入。在这简单介绍下挂钩和代码注入的方法和两个库，以及针对《刀塔传奇》实现的代码注入。

###利用libinject实现so注入和API Hook###

一. so注入

 Linux上有一个强大的系统调用ptrace,它提供了父进程观察和控制子进程的能力，并允许父进程检查和替换子进程寄存器的值（大名鼎鼎的gdb也是基于ptrace的），当使用ptrace后，发送给子进程的信号会转发给父进程，而子进程会被阻塞，父进程收到信号后，就可以对子进程进行检查和修改。其原型为：

	long ptrace(enum __ptrace_request request, pid_t pid, void *addr, void *data);
	
	1). enum __ptrace_request request：ptrace要执行的命令。
	2). pid_t pid: 指示ptrace要跟踪的进程。
	3). void *addr: 指示要监控的内存地址。
	4). void *data: 存放读取出的或者要写入的数据。

在获得root权限的情况下，我们可以再Android上ptrace另一个进程，读取和修改该进程的内存数据。看雪论坛上有大神实现了[Android下的so注入libinject](http://bbs.pediy.com/showthread.php?t=141355),代码的大致原理：

1. ptrace attack到目标进程，保持寄存器数据，接管程序的运行。

2. 找到目标进程的mmap函数地址，调用mmap分配一段内存空间。

3. 找到目标进程的dlopen、dlclose、dlsym的地址，调用dlopen载入.so文件，调用dlsym获取.so文件的地址。

4. 找到so中” hook_entry”函数的地址并执行。

5. 收尾，调用dlclose，还原寄存器，执行ptrace_detach，把控制权还给目标程序。

libinject中有两个主要功能（寻找函数地址和调用函数），函数分别为`get_remote_addr`和`ptrace_call_wrapper`，代码如下：

	{%highlight C++ %}
	void* get_remote_addr(pid_t target_pid, const char* module_name, void* local_addr)    
	{    
	    void* local_handle, *remote_handle;    
	    
	    local_handle = get_module_base(-1, module_name);    
	    remote_handle = get_module_base(target_pid, module_name);    
	    
	    DEBUG_PRINT("[+] get_remote_addr: local[%x], remote[%x]\n", local_handle, remote_handle);    
	    
	    void * ret_addr = (void *)((uint32_t)local_addr + (uint32_t)remote_handle - (uint32_t)local_handle);    
	    
		#if defined(__i386__)    
	    if (!strcmp(module_name, libc_path)) {    
	        ret_addr += 2;    
	    }    
		#endif    
	    return ret_addr;    
	} 

	int ptrace_call_wrapper(pid_t target_pid, const char * func_name, void * func_addr, long * parameters, int param_num, struct pt_regs * regs)     
	{    
	    DEBUG_PRINT("[+] Calling %s in target process.\n", func_name);    
	    if (ptrace_call(target_pid, (uint32_t)func_addr, parameters, param_num, regs) == -1)    
	        return -1;    
	    
	    if (ptrace_getregs(target_pid, regs) == -1)    
	        return -1;    
	    DEBUG_PRINT("[+] Target process returned from %s, return value=%x, pc=%x \n",     
	            func_name, ptrace_retval(regs), ptrace_ip(regs));    
	    return 0;    
	}   
	{% endhighlight %}


so的地址是通过分析/proc/pid/maps文件得到的。 Maps文件如下：

![](/assets/blog_pic/so_address.PNG)

在arm处理器下，执行函数的代码如下：

	{% highlight C++ %}	
	#elif defined(__i386__)    
	long ptrace_call(pid_t pid, uint32_t addr, long *params, uint32_t num_params, struct user_regs_struct * regs)    
	{    
	    regs->esp -= (num_params) * sizeof(long) ;    
	    ptrace_writedata(pid, (void *)regs->esp, (uint8_t *)params, (num_params) * sizeof(long));    
	    
	    long tmp_addr = 0x00;    
	    regs->esp -= sizeof(long);    
	    ptrace_writedata(pid, regs->esp, (char *)&tmp_addr, sizeof(tmp_addr));     
	    
	    regs->eip = addr;    
	    
	    if (ptrace_setregs(pid, regs) == -1     
	            || ptrace_continue( pid) == -1) {    
	        printf("error\n");    
	        return -1;    
	    }    
	    
	    int stat = 0;  
	    waitpid(pid, &stat, WUNTRACED);  
	    while (stat != 0xb7f) {  
	        if (ptrace_continue(pid) == -1) {  
	            printf("error\n");  
	            return -1;  
	        }  
	        waitpid(pid, &stat, WUNTRACED);  
	    }  
	    
	    return 0;    
	}  
	{% endhighlight %}

把返回地址设置为0的目的是让目标进程继续执行完后找不到返回地址出错，进程会被挂起，控制权又回到了父进程也就是libinject手上。

二. API Hook

api hook技术有2种elf hook 和inline hook。Elf hook 通过修改动态连接库的PLT/GOT表，从而达到函数调用的重定向目的，这种方法只能hook模块的外部调用，例如hook打开文件的系统函数检测程序打开文件的情况，hook系统时间相关的函数，达到加速的目的（市面上的加速外挂基本都是采取这种方法）。但是这种方法不能hook模块的内部调用，因为模块内部调用不需要查GOT表。而游戏引擎的功能都封装在一个动态连接库里，基本都是内部调用，ELF HOOK无法生效。本文所采用的是另外一个方法：INLINE HOOK。

 INLINE HOOK的思路大致是这样：首先找到目标函数在内存中的地址，然后把该地址块设置为可写，修改目标函数地址的内容，让游戏调用目标函数时跳转到我们自己的函数地址，我们的函数执行完后再跳转回来。这样不论是模块内部调用或外部调用，INLINE HOOK都能生效。具体步骤如下：

 1. 找到目标函数在内存中的地址，跟上文提到的寻找函数地址的方法不一样，注入so后，我们的代码是在目标进程空间中执行的，无法通过so基址的偏移计算函数在内存的地址，因为目标so在内存中只有一份。通过另外一种方式寻找函数地址，在linux下，可执行文件和动态连接库都是使用ELF文件格式的，ELF结构体中包含了所有符号的信息，通过解析ELF，可以获取到目标函数在内存中的地址。ELF文件格式这里就不介绍，感兴趣的同学可以查看[ELF文件介绍](http://staff.ustc.edu.cn/~sycheng/sst/exp_crack/ELF.pdf)。

 2. 代码段加载进内存后，一般不需要修改，所以代码段是没有写属性的，需要调用mprotect()把内存块加上PROT_WRITE属性。

 3. 接下来就可以把汇编指令写入指定地址了，以Arm指令集为例，把目标函数的头12个字节（ARM每条指令32位，即4个字节）先备份下来，然后替换成如下内容：

0xe59ff000,  ldr pc, [pc, #0]  ; 跳转到hook_func处开始执行 (ARM模式下,由于采用多级流水线结构,PC实际值为当前指令地址+8)

0xe1a08008,  同 nop。

hook_func， hook函数的地址。

当执行到我们的目标函数时，会被跳转到目标函数地址+2的位置，也就是我们的hook函数。在我们的hook函数里先把目标函数的头12个字节还原，然后再调用目标函数，调用完后再把头12个字节修改回来。关键代码如下：

	{% highlight C++ %}	
	unsigned int orig=0;  
	unsigned int store[3] = {0,0,0};  
	int jump_code[3] = {0xe59ff000, 0xe1a08008, 0};  
	//addr:目标函数地址，hookf:hook函数。  
	int hook_direct(unsigned int addr, void *hookf) 
	{  
		//设置hook函数 
	    jump_code[2] = (unsigned int)hookf; 
	    orig = addr;//保持好目标函数的地址  
		//备份前3个int
	    for (i = 0; i < 3; i++)  
	        store[i] = ((int*)addr)[i];  
	    for (i = 0; i < 3; i++)  
			//修改为我们的跳转指令
	        ((int*)orig)[i] = jump_code[i]   
	    return 1;  
	}  
	void hook_func()//hook函数  
	{  
	    printf(“hello\n”);
		//还原目标函数的头12个字节   
	    for (i = 0; i < 3; i++)  
	        ((int*)orig)[i] = store[i]  
	    void(*orig_func)() = (void*)orig;  
	    orig_func();//执行目标函数  
		//重新修改目标函数的头12个字节。
	    for (i = 0; i < 3; i++)   
	        ((int*)orig)[i] = jump_code[i];  
	}  
	{% endhighlight %}

这种方式没有处理函数的返回值，如果目标函数有返回值的话就会有问题。严谨的做法如下：

	{% highlight C++ %}	
	int jump_pre_code[12] = {  
	      0xe92d0008, 0xe1a0300f, 0xe283301c, 0xe583e000, 0xe89d0008,   
	      0xe28dd004, 0xe1a0e00f, 0xe59ff008, 0xe59fe000, 0xe1a0f00e,0,0  
	    };  
	Jump_pre_code[11]= (unsigned int)hookf;  
	for(int i = 0; i<12; i++)
	     jump_code[i+2] = jump_pre_code[i]; 
	{% endhighlight %} 

jump_pre_code所对应的汇编指令如下：

	stmdb sp!, {r3}     ; 将r3压入栈中,保存r3因为后边要修改r3,栈顶指针-1;  
	mov r3, pc          ; 将4指令所在地址赋给r3  
	add r3, r3, #0x1C   ; 将r3加上0x1c即从4指令所在地址往下7条指令,即就是jump_pre_code[10]赋给r3  
	str lr, [r3]        ; 将调用原函数的返回地址存入jump_pre_cod[10]中  
	ldmia sp, {r3}      ; 从栈中取出之前保存的r3  
	add sp, sp, #4      ;还原调用栈  
	mov lr, pc          ; 将返回地址存入lr中  
	ldr pc, [pc, #0x8]  ; 将10指令所在地址往下2条指令处的内容赋给pc,即PC跳到hookf我们自定义的hook函数  
	ldr lr, [pc, #0]    ; 执行完我们自定的hook函数后就会返回到这了,此处将当前指令往下2条指令出的内容即jump_pre_cod[10]取出赋给lr,即还原原先调用者的返回地址  
	mov pc, lr          ; 跳到原调用者的返回地址去  
	addr_ret        ;存放原函数的返回值  
	hookf               ;hook函数  


###利用adbi实现对《刀塔传奇》so注入和API Hook###

对于Android下的inject和hook，github上有个[adbi](https://github.com/crmulliner/adbi)框架。这个框架所使用的方法和上面介绍的差不多，采用inline hook但是没有处理返回值的情况，根据刚才介绍的方法，可以把返回值处理的功能加上，Thumb指令集的hook有个BUG，没有正确的跳转到hook函数的地址，跳转地址少了算2个字节，应该是jumpt[18]到jumpt[21]这4个字节存放hook_func的地址。

该框架包括2个模块：hijack和instruments，hijack编译出来后是一个可执行文件，用来注入动态链接库的。Instruments里包括base和example，example是一个hook的例子，编译出来是一个so文件。

《刀塔传奇》是利用cocos2d-x+lua编写的游戏，我们可以利用[adbi](https://github.com/crmulliner/adbi)实现对cocos2dx+lua中常用的函数如`lua_pushstring`的inject和hook从而来执行我们自己的lua脚本。`lua_pushstring`的声明如下：

	LUA_API void (lua_pushstring) (lua_State *L, const char* str);

基本思路是拿到lua 虚拟机的地址，然后调用luaL_loadstring和lua_call就可以在游戏进程中执行我们自己的lua脚本。主要代码如下：

	{% highlight C++ %}	
	int (*my_lua_call)(lua_State *, int, int) = NULL;  
	int (*my_luaL_loadstring)(lua_State*, const char *) =NULL;  
	void my_lua_pushstring (lua_State *L, const char* str);//目标进程lua_pushstring的hook函数，程序调用lua_pushstring时会先调用它  
	{  
	    int (*orig_lua_isuserdata)(lua_State *L, int idx);  
		//得到原函数 
	    orig_lua_pushstring = (void*)eph.orig;  
	    log("start hook func..precall...\n");  
	    hook_precall(&eph);  //还原原函数首地址  
	    orig_lua_pushstring (L, str);//调用原函数。  
	    if (counter) {  
	        log("lua_pushstring() called\n");  
	        counter--;  
	        if (!counter)  
	            log("removing hook for lua_pushstring ()\n");  
	    }  
		//如果找到了lua_call和luaL_loadstring的话就执行自己的lua代码。
	    if(my_lua_call!=NULL&&my_luaL_loadstring!=NULL)   
	    {  
	        my_luaL_loadstring(L, LUACODE);  
	        my_lua_call(L,0,0);  
	    }  
	    hook_postcall(&eph);//备份  
	}  
	void my_init(void) //so注入成功后会调用这个函数  
	{  
	    counter = 3;  
	  
	    log("%s my_init started\n", __FILE__);  
	    set_logfunction(my_log);  
	    unsigned long int lua_call_addr;  
	    unsigned long int lua_loadstring_addr;  
		//在进程中找lua_call函数地址 
	    find_name(getpid(),"lua_call", soname, &lua_call_addr);  
		//在目标进程中找luaL_loadstring函数地址.
	    find_name(getpid(), "luaL_loadstring",soname, 
		&lua_loadstring_addr);  
	    my_lua_call = lua_call_addr;  
	    my_luaL_loadstring = lua_loadstring_addr;  
	    log("lua_call addr:%p, luaL_loadstring addr:%p\n", lua_call_addr, lua_loadstring_addr);  
		//执行hook。
	    hook(&eph, getpid(), soname, "lua_pushstring", my_lua_pushstring_arm, my_lua_pushstring);  
	}  
	{% endhighlight %} 


（1）adbi主要包括hijack和libbase。Hijack提供了代码注入的功能，libbase提供了挂钩和卸载钩子的功能。

（2）编译adbi。主要是利用Android的NDK分别编译hijack和libbase，编译过后会生成一个libexample.so文件，并保存到/data/local/tmp/目录下，赋予执行权限，如下图：

![](/assets/blog_pic/push_so.png)

（3）查找所需挂钩游戏的so文件，可以通过两种方式，一种是解压apk文件查看lib目录下的so文件，另一种是使用命令“cat /proc/PID/maps”查看。如图显示了部分so文件：

![](/assets/blog_pic/so_address.PNG)

（4）保存执行hijack命令，如下图所示，其中776是《刀塔传奇》的进程ID。

![](/assets/blog_pic/hijack.png)

（5）运行《刀塔传奇》，在游戏调用lua_pushstring函数时，会跳转执行自己的函数，主要函数功能如下：

	local function Run20()
	    local label = CCLabelTTF:create("hello cocos2.x", "Arial", 60)
	    local MenuItem = CCMenuItemLabel:create(label)
	    MenuItem:registerScriptTapHandler(MainMenuCallback)
	    local s = CCDirector:sharedDirector():getWinSize()
	    local Menu = CCMenu:create()
	    Menu:addChild(MenuItem)
	    Menu:setPosition(100, 100)
	    MenuItem:setPosition(250, 25)
	    local scene = CCDirector:sharedDirector():getRunningScene()
	    scene:addChild(Menu)
	    Menu:setZOrder(99999999)
	    log("crate menuitem......")
	end

（6）执行上述代码的效果如下图（使用的是MTL的HTC手机）

![](/assets/blog_pic/daota.png)


参考：

[Android中的so注入(inject)和挂钩(hook)](http://blog.csdn.net/jinzhuojun/article/details/9900105)

[发个Android平台上的注入代码](http://bbs.pediy.com/showthread.php?t=141355)


