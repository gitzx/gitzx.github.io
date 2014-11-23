---
date: 2014-11-22 15:22:30+00:00
layout: post
title: lua中metatable和metamethod小结
thread: 87
categories: cocos2d-x
tags: cocos2d-x
---

元表(metatable)和元方法(metamethod)是lua中的基本概念，是扩展lua操作、lua库以及其他高级特性如面向对象、弱引用、垃圾回收等基础，在这小结下元表和元方法的基本使用。

###基本知识###

和其他语言一样，lua中每个值都有一些预定义的操作。通过元表(metatable)修改一个值的行为，可以在面对一个非预定义的操作时执行一个指定的操作。

例如执行两个table相加时，由于table中没有预定义，执行时会先检查两者之一是否有元表(metatable)，然后检查该元表是否有一个叫`__add`的字段，若有该字段，则调用该字段对应的值，调用该字段执行加法操作就是元方法(metamethod)，"add"操作就是event.

lua中每个值都有一个元表，除了table和userdata可以有各自独立的元表，其他类型的值共享其类型所属的单一元表。

在lua代码中，只能设置table的元表，其他类型值的元表，需要通过C代码来完成。

设置和查看元表的方法分别是`setmetatable`和`getmetatable`:

	--创建新table不会创建元表
	t={}
	print(getmetatable(t))  --nil 
	
	--可通过setmetatable来设置修改table元表
	t1={}
	setmetatable(t,t1)
	assert(getmetatable(t)==t1)

table可以作为任何值的元表，如多个table共享一个元表、作为自己的元表等等。

###元方法分类###

介绍完元表，再小结下元方法，常用的元方法有19个，这些元方法的主要可分为：

- 算术类元方法.  `__unm`，`__add`， `__sub`， `__mul`， `__div`， `__mod`， `__pow`， `__concat`， `__len`

- 关系类元方法.  `__eq`, `__lt`, `__le`

- table访问的元方法. `__index`, `__newindex`

- 库定义的元方法.  `__tostring`,  `__metatable`

- 其他元方法.  `__call`, `__mode`, `__gc`

下面对这些元方法进行简单示例，实际的行为已经硬编码在解释器中，且效率更高。提取对象中元方法的表达式为`metatable(obj)[event]`,可以理解为`rawget(getmetatable(obj) or {}, event)`。对于lua的二元操作，可以使用`getbinhandler`函数：

	{% highlight lua %}
	function getbinhandler(op1, op2, event)
		return metatable(op1)[event] or metatable(op2)[evetn]
	end
	{% endhighlight %}

###算术类元方法###

	{% highlight lua %}
	-- unm 取反操作
	function unm_event(op)
		local o = tonumber(op)
		if o then
			return -o
		else
			local h = metatable(op).__unm
			if h then
				return (h(op))
			else
				error("cannot unm")
			end
		end
	end
	
	-- add 加法操作
	function add_event(op1, op2)
		local o1, o2 = tonumber(op1), tonumber(op2)
		if o1 and o2 then
			return o1+o2
		else
			local h = getbinhandler(op1, op2, "__add")
			if h then 
				return (h(op1, op2))
			else
				error("cannot add")
			end
		end
	end
	
	-- sub 加法操作
	function sub_event(op1,op2)
		local o1, o2 = tonumber(op1), tonumber(op2)
		if o1 and o2 then 
			return o1-o2
		else
			local h = getbinhandler(op1, op2, "__sub")
			if h then 
				return (h(op1, op2))
			else
				error("cannot sub")
			end
		end
	end
	
	-- mul 乘法操作
	function mul_event(op1,op2)
		local o1, o2 = tonumber(op1), tonumber(op2)
		if o1 and o2 then
			return (o1)*(o2)
		else 
			local h = getbinhandler(op1, op2, "__mul")
			if h then 
				return (h(op1, op2))
			else
				error("cannot mul")
			end
		end
	end
	
	-- div 除法操作
	function div_event(op1, op2)
		local o1, o2 = tonumber(op1), tonumber(op2)
		if o1 and o2 then 
			return (o1)/(o2)
		else
			local h = getbinhandler(op1, op2, "__div")
			if h then 
				return (h(op1, op2))
			else
				error("cannot div")
			end
		end
	end
	
	-- mod 取模操作
	function mod_event(op1, op2)
		local o1, o2 = tonumber(op1), tonumber(op2)
		if o1 and o2 then
			return (o1)%(o2)
		else
			local h = getbinhandler(op1,op2,"__mod")
			if h then 
				return (h(op1, op2))
			else
				error("cannot mod")
			end
		end
	end
	
	-- pow 指数操作
	function pow_event(op1, op2)
		local o1, o2 = tonumber(op1), tonumber(op2)
		if o1 and o2 then
			return (o1)^(o2)
		else
			local h=getbinhandler(op1,op2,"__pow")
			if h then 
				return h((op1, op2))
			else
				error("cannot pow")
			end
		end
	end
	
	-- concat 连接操作
	function concat_event(op1,op2)
		if(type(op1)=="string" or type(op1)=="number") and
			(type(op2)=="string" or type(op2)=="number") then
			return op1 .. op2
		else
			local h = getbinhandler(op1,op2,"__concat")
			if h then 
				return (h(op1,op2))
			else
				error("cannot concat")
			end
		end
	end
	
	-- len 取长操作
	function len_event(op)
		if type(op)=="string" then
			return strlen(op)
		else
			local h=metatable(op).__len
			if h then
				return (h(op))
			elseif type(op)=="table" then
				return #op
			else
				error("cannot len")
			end
		end
	end	
	{% endhighlight %}


###关系类元方法###

	{% highlight lua %}
	-- eq 相等操作
	function eq_event(op1, op2)
		if type(op1)=="number" and type(op2)=="number" then
			return op1==op2
		elseif type(op1)=="string" and type(op2)=="string" then
			return op1==op2
		else
			local h=getbinhandler(op1,op2,"__eq")
			if h then
				return not not (h(op1, op2))
			else
				error("not eq")
			end
		end
	end
	
	--lt 小于操作 
	function lt_event(op1, op2)
		if type(op1)=="number" and type(op2)=="number" then
			return op1<op2
		elseif type(op1)=="string" and type(op2)=="string" then
			return op1<op2
		else
			local h=getbinhandler(op1,op2,"__lt")
			if h then
				return not not (h(op1, op2))
			else
				error("not eq")
			end
		end
	end
	
	-- le 小于等于操作
	function lt_event(op1, op2)
		if type(op1)=="number" and type(op2)=="number" then
			return op1 <= op2
		elseif type(op1)=="string" and type(op2)=="string" then
			return op1 <= op2
		else
			local h=getbinhandler(op1,op2,"__le")
			if h then
				return not not (h(op1, op2))
			else
				h=getbinhandler(op1, op2, "__lt")
				if h then
					return not (h(op2, op1))
				else
					error("not eq")
				end
			end
		end
	end
	{% endhighlight %}

###table访问的元方法###

	{% highlight lua %}
	-- index 访问table[key]
	function gettable_event(table, key)
		local h
		if type(table)=="table" then
			local v=rawget(table, key)
			if v~=nil then 
				return v
			end
			h=mettable(table).__index
			if h==nil then 
				return nil
			end
		else
			h=metatable(table).__index
			if h==nil then
				error("not table and is nil")
			end
		end
		if type(h)=="function" then
			return (h(table, key))
		else
			return h[key]
		end
	end
	
	-- newindex 访问table[key]=value操作
	function settable_event(table, key, value)
		local h
		if type(table)=="table" then
			local v=rawget(table, key)
			if v~=nil then
				rawset(table, key, value)
				return 
			end
			h=metatable(table).__newindex
			if h==nil then
				rawset(table, key, value)
				return 
			end
		else
			if type(h)=="function" then
				h(table, key ,value)
			else 
				h[key]=value
		end
	end
	{% endhighlight %}

参考：

[Metatable Events](http://lua-users.org/wiki/MetatableEvents)

[Lua 5.2 Reference Manual](http://www.lua.org/manual/5.2/manual.html#2.4)
