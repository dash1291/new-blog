------
"title": "Setting up Eclipse as your C/C++ environment"
"layout": "post"
-------

Eclipse is an awesome and seemingly the best IDE when it comes to Android, Java and PHP development. Well, it becomes excrutiating when we use an obsolete compiler for C/C++ or a compiler which is complicated as might be the case in a command line based gcc compiler. Talking about IDEs for C/C++, MS VC++ beats all odds, but then its beaten off by its own drawback of not being a cross-platform programming environment and being so Windows. This is where Eclipse starts ruling the stage. Eclipse being a highly flexible IDE, can support various developing languages and platforms, C/C++ not being among the exceptions. One can download the CDT plugin(c/c++ development tools) from the Eclipse's website and integrate it with their Eclipse environment to start using Eclipse for C/C++ development. It uses the GNU based C tools to compile the code developed using c/c++ so make sure you have gcc installed in your computer. So I would just enlist the steps in brief to configure your Eclipse environment with CDT plugin.

If you dont have Eclipse already installed, you can simply download the pre-configured IDE. [Download Link](http://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/heliossr2)
Otherwise,follow these steps,

1. Make sure you have gcc installed in your computer.
2. Download the CDT plugin. [Download Link](http://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/heliossr2)
3. Add your CDT plugin by going into Install New Software option that can be found in the help menu and browse the zip file of the CDT plugin that you downloaded.
4. Thats it, start coding.
