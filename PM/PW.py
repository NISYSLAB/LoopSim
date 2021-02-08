import requests
import logging
logging.basicConfig(level=logging.INFO)

def test():
    out_text = 0.0
    earlier_text = 0.0
    later_text = 0.0
    no_skip = True

    # We just repeating 100 times.
    i = 0
    while i < 100:
        if no_skip:
            i = i + 1

            # This should computation and file actually come from PM
            # Currently we are manually changing it for the prototype.
            # Eventually PW does not change the data.
            # Reads u. Writes ym. ym = f(u)
            f = open('./u', "r")

            # This is where we get the u value before the return file.
            earlier_text = float(f.read().strip())

            f.close()
            out_text = earlier_text + 3.0
            f = open('./ym', "w")
            f.write(str(out_text))
            f.close()

        files = {'file1': open('./ym', 'rb')}

        # POST Request to /pm with ym as file1
        r = requests.post('http://localhost/ctl', files=files)

        # output is supposedly the new "u". Maybe not. Let's check.
        logging.info(r.content)
        try:
            later_text = float(r.content)
            # new u is different from previous u. This calls for execution of PM.
            if earlier_text != later_text:
                no_skip = True
                with open('./u','wb') as output:
                    output.write(r.content)
                    earlier_text = later_text
            else:
                no_skip = False
        except ValueError:
            no_skip = False

f = open('./ym', "w")
f.write('1.0')
f.close()
files = {'file1': open('./u', 'rb')}
r2 = requests.post('http://localhost/ctl', files=files)

if __name__ == '__main__':
    test()
