# jlmacro
Inline macros written in python in comments. 

 1. Start the macro section with the comment 
 ``//jlmacro --input``

 1. Within the macro section use python code to add content to the variable ``result``
``//result = `std::cout << "Hello world" << std::endl;`

 1. End the inline section with the comment
``//jlmacro --output``

 1. The content added to result will be added here.

 1. End the output section with the comment 
``//jlmacro --end`

 1. Call jlmacro on the source file and the output sections will be updated with the results of the input sections.
``python3 jlmacro.py ../project/src/test.cpp``

Sections can reference variables or functions defined in previous macro blocks.
