import sys
import s3writer
import datetime
import textwrap


class cowstatus(object):
    
    def __init__(self):
        self.s3=s3writer.s3writer()
        self.start=datetime.datetime.now()

    def cowsay(self, str, length=40):
        return self.build_bubble(str, length) + self.build_cow()

    def build_cow(self):
        return """
             \   ^__^ 
              \  (oo)\_______
                 (__)\       )\/\\
                     ||----w |
                     ||     ||
        """

    def build_bubble(self, str, length=40):
        bubble = []

        lines = self.normalize_text(str, length)

        bordersize = len(lines[0])

        bubble.append("  " + "_" * bordersize)

        for index, line in enumerate(lines):
            border = self.get_border(lines, index)

            bubble.append("%s %s %s" % (border[0], line, border[1]))

        bubble.append("  " + "-" * bordersize)

        return "\n".join(bubble)

    def normalize_text(self, str, length):
        lines  = textwrap.wrap(str, length)
        maxlen = len(max(lines, key=len))
        return [ line.ljust(maxlen) for line in lines ]

    def get_border(self, lines, index):
        if len(lines) < 2:
            return [ "<", ">" ]

        elif index == 0:
            return [ "/", "\\" ]
    
        elif index == len(lines) - 1:
            return [ "\\", "/" ]
    
        else:
            return [ "|", "|" ]
        
    def uptime(self):
        delta=self.start-datetime.datetime.now()
        days=delta.days
        s=delta.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        return(days,hours,minutes,seconds)
    
    def update_status(self, count):
        header="<html><body><pre>\n"
        status="Uptime: %d days, %d hours %d min, %d sec \n"%self.uptime()
        status+="Absorbed %d messages"%count
        footer="</pre></body></html>"
        self.s3.write("stats.html",header+self.cowsay(status)+footer)
        #print(self.cowsay(status))
    