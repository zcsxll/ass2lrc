import os
import re

class Dialogue:
    def __init__(self, sh=0, sm=0, ss=0.00, chinese='', englisg=''):
        self.sh = sh
        self.sm = sm
        self.ss = ss
        self.chinese = chinese
        self.english = englisg

    def set_ass(self, str_ass):
        # print('[%s]' % str_ass)
        ss = str_ass.split(',')
        # print(ss)
        assert len(ss) >= 10
        self.get_start_time(ss[1])

        origin = ss[9]
        for s in ss[10:]:
            origin += (",%s" % s)
        self.get_content(origin)

    def get_start_time(self, s):
        ss = s.split(':')
        # print(ss)
        assert len(ss) == 3
        self.sh = int(ss[0])
        self.sm = int(ss[1])
        self.ss = float(ss[2])

    def get_content(self, s):
        # print(s)
        # s.replace('{*}', '')
        # print(s)
        # a = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)
        content = re.sub('{.*?\\}', '', s)
        # print(content)
        ss = content.split('\\N')
        # assert len(ss) <= 2
        if len(ss) == 1:
            self.chinese = ss[0]
            self.english = ''
        else:
            self.chinese = ss[0]
            for s in ss[1:-1]:
                self.chinese += s
            self.english = ss[-1]

    def get_time(self):
        return self.sh * 60 * 60 + self.sm * 60 + self.ss

    def get_lrc(self, off_s):
        assert self.sh == 0
        s = self.sm * 60 + self.ss + off_s
        sm = s // 60
        ss = s - sm * 60
        ret = "[%d:%.2f]%s # %s" % (sm, ss, self.english, self.chinese)
        return ret

class Ass2Lrc:
    def __init__(self):
        self.dialogue = Dialogue()
        self.off_s = -1

    def process(self, file_in_ass, file_out_lrc):
        print(file_in_ass)
        pf = open(file_in_ass, encoding='utf-8')
        pf_lrc = open(file_out_lrc, mode='w', encoding='utf-8')
        for idx, line in enumerate(pf):
            line = line.strip()
            if not line.startswith('Dialogue:'):
                continue
            # print(line)
            self.dialogue.set_ass(line[10:])
            # if idx > 50:
            #     break
            if self.off_s < 0:
                self.off_s = self.dialogue.get_time()
            line = self.dialogue.get_lrc(-self.off_s)
            # print(line)
            pf_lrc.write("%s\n" % line)
        pf.close
        pf_lrc.close()

def zcs(dir_ass, dir_lrc):
    sub_dirs = os.listdir(dir_ass)
    for sub_sir in sub_dirs:
        dir1 = os.path.join(dir_ass, sub_sir)
        asses = os.listdir(dir1)
        for ass in asses:
            # print(ass)
            s = int(ass[9:11])
            e = int(ass[12:14])
            # print(s, e)
            ass = os.path.join(dir1, ass)
            lrc = "Friends%d%02d.lrc" % (s, e)
            lrc = os.path.join(dir_lrc, lrc)
            # print(lrc)
            Ass2Lrc().process(ass, lrc)
        # break

if __name__ == "__main__":
    # file = './Friends.ass/Friends.S01.1994/Friends.S01E01.1994.BluRay.1080p.x265.10bit.MNHD-FRDS.ass'
    # file_lrc = './Friends.lrc/Friends101.lrc'
    # Ass2Lrc().process(file, file_lrc)

    zcs('Friends.ass', 'Friends.lrc')