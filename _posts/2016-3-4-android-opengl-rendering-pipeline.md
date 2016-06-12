---
date: 2016-3-4 8:12:30+00:00
layout: post
title: Android环境下OpenGL的初始化和渲染
thread: 99
categories: android opengl
tags: android opengl
---

渲染管线(rendering pipeline)是一系列数据处理过程，并且将应用程序的数据转换到最终渲染的图像。OpenGL实现了渲染管线。好久没更新了，在这简单介绍下Android环境下OpenGL的初始化和渲染。

###GPU图形绘制管线###

图形绘制管线分为三个阶段：（1）应用程序阶段；（2）几何阶段；（3）光栅阶段。

1. 几何阶段

几何阶段的主要工作是“变换三维顶点坐标”和“光照计算”。GPU需要将三维的数据，绘制到二维的屏幕上。根据顶点坐标变换的先后顺序，主要有如下几个坐标空间：

 （1）模型坐标空间(object space): 模型文件的顶点值，建模得到；与其他物体没有任何参照关系；

 （2）世界坐标空间(World space)：相对于原点的位置；关照计算通常在世界坐标空间进行；

 （3）观察坐标空间(Eye space)；以camera为原点，由视线方向、视角和远近平面共同组成的一个梯形体的三维空间(视椎)；

 （4）屏幕坐标空间(clip and project space).

2. 光栅化阶段

光栅化：决定哪些像素被集合图元覆盖的过程，经过上面坐标转换之后，我们得到了平面坐标值，也知道了我们需要绘制的图元(点、线、面)。


###OpenGL渲染管线###

OpenGL渲染管线操作和GPU的类似，可以分为以下几个部分：

 (1)指定几何对象；

 (2)顶点操作处理；

 (3)图元装配；

 (4)图元处理(裁剪、消隐)；

 (5)栅格化操作；

 (6)片元处理；

 (7)逐个片元操作；

 (8)帧缓冲操作。


###Android环境下OpenGL的初始化和渲染###


Android支持OpengGL ES 1.x版本至3.x版本，由于兼容性问题，通常使用的是OpenGL ES2.x版本。Android有两种方法使用OpenGL ES，在这主要介绍第二种。:

 (1)通过NDK调用OpenGL ES接口；

（2）使用Android框架接口来调用OpenGL ES接口。


####GLSurfaceView和GLSurfaceView.Render####

GLSurfaceView是个View类，类似于android的SurfaceView；GLSurfaceView.Render则基于GLSurfaceView绘制图形。使用GLSurfaceView.Render需实现如下3个基本的方法：

（1）onSurfaceCreated(): 在创建GLSurfaceView时调用，系统仅调用一次；

（2）onDrawFrame():每次绘制或重绘GLSurfaceView时调用；

（3）onSurfaceChanged():GLSurfaceView的几何参数发生变化(如尺寸或方向)时调用。


    public void onSurfaceCreated(GL10 glUnused, EGLConfig config)
    {
        glClearColor(1.0f, 0.0f, 0.0f, 0.0f);
        String vertexShaderSource = TextResourceReader.readTextFileFromResource(context, R.raw.simple_vertex_shader);
        String fragmentShaderSource = TextResourceReader.readTextFileFromResource(context, R.raw.simple_fragment_shader);
        int vertexShader = ShaderHelper.compileVertexShader(vertexShaderSource);
        int fragmentShader = ShaderHelper.compileFragmentShader(fragmentShaderSource);
        program = ShaderHelper.linkProgram(vertexShader, fragmentShader);
        if (LoggerConfig.ON) {
            ShaderHelper.validateProgram(program);
        }
        glUseProgram(program);
        uColorLocation = glGetUniformLocation(program, U_COLOR);
        aPositionLocation = glGetAttribLocation(program, A_POSITION);
        vertexData.position(0);
        glVertexAttribPointer(aPositionLocation, POSITION_COMPONENT_COUNT, GL_FLOAT,
                false, 0, vertexData);

        glEnableVertexAttribArray(aPositionLocation);
    }

    @Override
    public void onSurfaceChanged(GL10 glUnused, int width, int height)
    {
        glViewport(0,0,width,height);
    }

    @Override
    public void onDrawFrame(GL10 glUnused)
    {
        glClear(GL_COLOR_BUFFER_BIT);

        // Draw the table.
        glUniform4f(uColorLocation, 1.0f, 1.0f, 1.0f, 1.0f);
        glDrawArrays(GL_TRIANGLES, 0, 6);

        // Draw the center dividing line.
        glUniform4f(uColorLocation, 1.0f, 0.0f, 0.0f, 1.0f);
        glDrawArrays(GL_LINES, 6, 2);

        // Draw the first mallet blue.
        glUniform4f(uColorLocation, 0.0f, 0.0f, 1.0f, 1.0f);
        glDrawArrays(GL_POINTS, 8, 1);

        // Draw the second mallet red.
        glUniform4f(uColorLocation, 1.0f, 0.0f, 0.0f, 1.0f);
        glDrawArrays(GL_POINTS, 9, 1);
    }



参考：[OpenGL ES应用开发实践指南(Android卷)]()

[ANDROID LESSON ONE: GETTING STARTED](http://www.learnopengles.com/android-lesson-one-getting-started/)
















