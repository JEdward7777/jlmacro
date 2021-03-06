import sys,os,re


def get_temp_name( filename ):
    return f"{filename}.jlmacro.tmp"


def run_file( jlm_file_to_run ):
    jlm_read_code = []
    jlm_in_input = False
    jlm_in_output = False
    jlm_eval_vars = {}

    jlm_temp_name = get_temp_name( jlm_file_to_run )
    with open( jlm_temp_name, "wt" ) as jlm_fout:
        with open( jlm_file_to_run, "rt" ) as jlm_fin:
            for jlm_line in jlm_fin:

                if jlm_line.startswith( "//jlmacro --input" ) or jlm_line.startswith( "//jlmacro --start" ):
                    jlm_fout.write( jlm_line )

                    jlm_in_input = True
                    jlm_in_output = False

                elif jlm_line.startswith( "//jlmacro --output" ):
                    jlm_fout.write( jlm_line )

                    #time to eval.
                    jlm_joined_code = "\n".join( jlm_read_code )
                    exec( jlm_joined_code, {}, jlm_eval_vars )
                    jlm_read_code = []

                    #now write the output from result in eval_vars
                    if "result" in jlm_eval_vars:
                        jlm_fout.write( jlm_eval_vars["result"] + "\n" )
                        jlm_eval_vars["result"] = ""

                    jlm_in_input = False
                    jlm_in_output = True
                elif jlm_line.startswith( "//jlmacro --end" ):
                    jlm_fout.write( jlm_line )

                    jlm_in_input = False
                    jlm_in_output = False
                
                elif jlm_in_input:
                    jlm_fout.write( jlm_line )

                    #if it isn't the file which is being pulled in, then we need to consume the input.
                    jlm_code = jlm_line.strip()
                    #remove the comment char at the beginning.
                    if "//" in jlm_code:
                        jlm_slash_pos = jlm_code.index( "//" )
                        jlm_code = jlm_code[jlm_slash_pos+2:]
                        jlm_read_code.append(jlm_code)

                elif jlm_in_output:
                    #don't copy the old output to the output.
                    pass

                else:
                    #Just pass through the rest of the file.
                    jlm_fout.write( jlm_line )


    #now copy the file back over.
    os.remove(jlm_file_to_run)
    os.rename(jlm_temp_name,jlm_file_to_run)


        


def main(args):
    for file_to_run in args:
        run_file( file_to_run)


    print( args )

if __name__ == '__main__':
    main(sys.argv[1:])