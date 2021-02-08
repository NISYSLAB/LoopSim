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

            # This should computation and file actually come from CM
            # Currently we are manually changing it for the prototype.
            # Eventually CW does not change the data.
            # Reads ym. Writes u. u = g(ym)
            f = open('./ym', "r")

            # This is where we get the u value before the return file.
            earlier_text = float(f.read().strip())

            f.close()
            out_text = earlier_text - 2.0
            f = open('./u', "w")
            f.write(str(out_text))
            f.close()

        files = {'file1': open('./u', 'rb')}

        # POST Request to /ctl with u as file1
        r = requests.post('http://localhost/pm', files=files)

        # output is supposedly the new "ym". Maybe not. Let's check.
        logging.info(r.content)
        try:
            later_text = float(r.content)
            # new ym is different from previous ym. This calls for execution of CM.
            if earlier_text != later_text:
                no_skip = True
                with open('./ym','wb') as output:
                    output.write(r.content)
                    earlier_text = later_text
            else:
                no_skip = False
        except ValueError:
            no_skip = False

f = open('./u', "w")
f.write('1.0')
f.close()
files = {'file1': open('./u', 'rb')}
r2 = requests.post('http://localhost/pm', files=files)

if __name__ == '__main__':
    test()
