import unittest
import re


'''
--- Day 7: Recursive Circus ---

Wandering further through the circuits of the computer, you come upon a tower
of programs that have gotten themselves into a bit of trouble. A recursive
algorithm has gotten out of hand, and now they're balanced precariously in a
large tower.

One program at the bottom supports the entire tower. It's holding a large disc,
and on the disc are balanced several more sub-towers. At the bottom of these
sub-towers, standing on the bottom disc, are other programs, each holding their
own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many
programs stand simply keeping the disc below them balanced but with no disc of
their own.

You offer to help, but first you need to understand the structure of these
towers. You ask each program to yell out their name, their weight, and (if
they're holding a disc) the names of the programs immediately above them
balancing on that disc. You write this information down (your puzzle input).
Unfortunately, in their panic, they don't do this in an orderly fashion; by the
time you're done, you're not sure which program gave which information.

For example, if your list is the following:

    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)

...then you would be able to recreate the structure of the towers that
looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and
is holding up ugml, padx, and fwft. Those programs are, in turn, holding up
other programs; in this example, none of those programs are holding up any
other programs, and are all the tops of their own towers. (The actual tower
balancing in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is
correct. What is the name of the bottom program?


--- Part Two ---

The programs explain the situation: they can't get down. Rather, they could get
down, if they weren't expending all of their energy trying to keep the tower
balanced. Apparently, one program has the wrong weight, and until it's fixed,
they're stuck here.

For any program holding a disc, each program standing on that disc forms a
sub-tower. Each of those sub-towers are supposed to be the same weight, or the
disc itself isn't balanced. The weight of a tower is the sum of the weights of
the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo,
ebii, and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and
all programs above it must each match. This means that the following sums must
all be the same:

    ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
    padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
    fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the
other two. Even though the nodes above ugml are balanced, ugml itself is too
heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the
towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need
to be to balance the entire tower?
'''

mstring = '(\S+) \((\d+)\)( -> )*(.+|)'


class Program:

    def __init__(self, lines=None):
        self.subs = []
        self._weight = 0
        self.feed(lines)

    def feed(self, lines):
        if lines:
            for line in lines:
                name, weight, leafs = re.match(mstring, line).group(1, 2, 4)
                self.insert([l.strip() for l in leafs.split(',')])

    def insert(self, prog, relations=None, weight=None):
        if not self.existing_node_update(prog, weight, relations):
            self.insert_new(prog, weight, relations)
        print(self)

    def __str__(self):
        return '{}({}): {}'.format(self._weight, [s for s in self.subs])

    def insert_new(self, prog, weight, relations):
        self.subs[prog] = Program()
        self.subs[prog].subs = self.gather_related_progs(relations)
        self.subs[prog]._weight = weight

    def existing_node_update(self, prog, weight, relations):
        match = self.find(prog, self)
        # TODO !!!!!!!!!!!!nonenotnone
        if match is not None:
            match.subs.update(self.gather_related_progs(relations))
            match._weight = weight
            return True
        return False

    def find(self, name, progs):
        if name and progs:
            if name in progs.subs:
                return progs.subs[name]
            else:
                for n in progs.subs:
                    match = self.find(name, progs.subs[n])
                    if match is not None:
                        return match
        return None

    def gather_related_progs(self, subs):
        progs = {}
        if subs:
            for n in subs:
                match = self.find(n, self)
                if match is not None:
                    progs[n] = match
                    self.subs.pop(n)
                else:
                    progs[n] = Program()
        return progs

    @property
    def name(self):
        if len(self.subs) != 1:
            raise AssertionError('Several Root nodes: {}'.format(self.subs))
        return next(iter(self.subs))

    @property
    def weight(self):
        w = 0
        if self.subs:
            for n in self.subs:
                w += n.weight
        return w

    def show(self):
        print(" {} ".format(self))


class TestDaySevenPartTwo(unittest.TestCase):

    def test_tower_weight(self):
        t = Program()
        t.insert('aaa', weight=123, relations=['bbb'])
        t.insert('ccc', weight=7)
        t.insert('bbb', weight=70, relations=['ccc'])
        self.assertEqual(200, t.weight)


@unittest.SkipTest
class TestDaySeven(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(re.match(mstring, 'xhth (57)').group(1, 2, 3, 4),
                         ('xhth', '57', None, ''))
        self.assertEqual(re.match(mstring, 'fwft (72) -> ktlj, cntj, xhth').group(1, 2, 4),
                         ('fwft', '72', 'ktlj, cntj, xhth'))

    def test_will_place_given_prog_to_subtower(self):
        t = Program()
        t.insert('aaa', ['bbb'])
        t.insert('bbb', weight=10)
        t.show()
        self.assertEqual(0, t.relations['aaa'].relations['bbb'].weight)

    def test_will_move_given_prog_to_subtower(self):
        t = Program()
        t.insert('bbb', weight=22)
        t.insert('aaa', ['bbb'])
        self.assertEqual(0, t.relations['aaa'].relations['bbb'].weight)

    def test_will_place_given_prog_deeper_in_subtower(self):
        t = Program()
        t.insert('ccc', ['ddd'])
        t.insert('bbb', ['ccc'])
        t.insert('aaa', ['bbb'])
        t.insert('ddd', weight=123)
        self.assertEqual(len(t.relations), 1)
        self.assertEqual(0, t.relations['aaa'].relations['bbb'].relations['ccc'].relations['ddd'].weight)

    def test_examples(self):
        t = Program(example.splitlines())
        self.assertEqual('tknk', t.name)

    def test_solution(self):
        t = Program(problem.splitlines())
        self.assertEqual('hmvwl', t.name)


example = '''\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
'''

problem = '''\
yjmbbu (75)
zdhvqrl (40) -> fpbsu, fwpfjjd, viqhfi
dywqvqh (9)
gewgn (31)
xfekjt (67)
zezowe (31)
wgqkdcr (79)
ljhwzvv (258)
vustse (1584) -> ffnabs, qinmi, qhafxnl
idfwjgx (112) -> buoakk, itwbpot
lxesg (71)
qkbnq (99)
jppgd (27)
ztghd (125) -> bcibchp, aaheijb
qcrpdy (29)
fwidkbp (152) -> mnkwo, ehjooz, jvccsp, cyrrjtx, imynb, chnkkj, agywjrs
nymhem (52)
cazid (93)
olspit (121) -> bqtas, fhuiyrl
ayteb (92)
hjucki (58)
wrqtk (305)
jfjemon (217) -> bjhickt, uacjhqx
mcmqliy (925) -> coopirx, ekohgo, ioywk
rsancy (70) -> aeuub, vchuc, heacb
zjwpbzs (23) -> jysaup, pgubexv, lckuoqf, eeguu
qflouyn (90)
nswximo (65478) -> ibjvonk, sdhtguj, dxyifeb
rymkqd (102) -> vgqeyx, zezowe
wlujpl (92) -> sjwhig, wymfopy, ylfsnz
imcczga (95)
xehdglb (52)
twubx (46) -> goimlra, vlimzz, xaoncma, gfzbp, spdhhoe, fhmauag, cyapi
yjhes (72)
ymcuygn (81)
yatbsip (19) -> bkdtinl, nzqcq, tkmed, ysbrui
yipoeia (58)
chophr (27)
tdwtlf (305) -> epuaii, idfwjgx, nwikpdm
emzrj (119) -> aimav, dtscjna
vbxmpc (7)
nrpxx (21)
wgexpa (103) -> paxzd, vgdwm
vnrmx (359) -> knzppj, gkkgkp, ttwfig, vcixs
knltna (677) -> zbhtee, ztzwh
ojvlwm (52)
bgflw (27)
lsdrwz (73)
hswzo (40)
spwgm (351) -> mizab, cyzkk
jlnyr (16)
nwikpdm (36) -> ihwaeuw, wwkeej
qbmtmcs (34)
djirpp (19)
pkfhp (59)
qfypnb (76)
jzequar (272) -> mtcrswx, wkcyd
tttle (71) -> xlskkfi, ayteb
zbhtee (48)
iriun (9)
dwezv (73)
tojyt (58) -> dwezv, nbngkou, wnjtb, rarkunn
bsorz (27)
qvkotfd (337)
azxjd (268) -> exeub, lryzkx, nqvxs
wpxxh (998) -> wrqtk, yosnw, vyxfljc
gwournc (85)
aghdlll (88)
lejgcu (19)
lxlbt (363) -> oiosol, mpchqe, bsorz, jbpjt
nbeagw (94)
vbbgeo (19)
lqfyzo (21) -> tggkm, zdbqs
vqclii (331) -> dmkbnot, omdpc
lhmnd (216) -> onnylx, khaupo
wwkeej (60)
laczal (99)
xrbjn (20)
qvteg (64)
ogbsm (92) -> xpzhy, mhsjkm
ymckwqo (41)
ghsjtj (271) -> hhmwlo, faixe
sjrxs (259) -> mnijdlk, hygfoe
hdvel (197) -> upuxd, dtstgj
lckuoqf (78)
yppydul (91)
frirj (6)
duftj (42)
dnmvzeg (64)
cpazlc (19)
krxyaak (198) -> maqgick, xbnmvd
oyczfgb (395) -> rxcnn, ktpte, qybmgto
oxiuaz (12)
wfphcf (6)
ihtnbb (87)
omsroa (45)
lybkeg (6022) -> oyczfgb, jzequar, yrcgsnx, ujulj
agywjrs (184) -> anpnrdt, hgdbaol, hcjmsd, kzbvrxk
tiujei (34)
lwencl (28) -> ieusgd, mthhq, fsuzqyz, miwoup, isrtfc
wekya (34)
bkdtinl (1167) -> ojsjuts, euoclfs, xbkeua, mykrcq, jjsvfy, aazxafl
qinmi (1896) -> qshbt, ruozmjk
yfmxvay (46)
kgpwo (52)
fgjjwep (14)
odvtiti (76)
ienye (19)
tcvabyz (99)
ycclns (7)
njogewi (30)
bfchbs (87) -> jykbb, qnbfk
dlbzng (99)
xnmvtem (51)
ccciux (94)
xwlmsqy (25)
wekkbw (17)
yipzce (21)
hcjmsd (10)
upvhfmn (68) -> fvlfq, ivmndi, ussmw, ccciux
hacwv (50)
redqvw (269)
dtpexjq (52)
kmlwj (84)
mluykm (19)
ucbbun (114) -> hrqzqqh, ccuarv
kymhbse (155) -> tznudmk, hnlgkv
xomnhw (185)
nsmoh (65) -> ceuygh, acpfsnb, vgubuy, apkwi, yoeau, pdosfg, lfpzff
zvepqr (51)
wnotwt (99)
lcrwbqi (27)
hdlqvlg (27)
iphgmyt (160) -> woolxv, ewyzqg
ujulj (50) -> cazid, npmwcx, yeooycn, dmeee
zjaklmn (52)
bjrpalu (53) -> rhodopg, tcospq, cvrcvgp
azdei (48)
snzfrer (149) -> bhsbd, tgdzl
zsxizw (18)
fwpfjjd (89)
fndxl (36)
uzrnud (14)
igyxt (41)
vxdkej (135) -> diomq, qokscr
gjuekv (5)
uzufet (143) -> fgjjwep, uzrnud
vzuqbye (87) -> eviqjr, cgxsmq, egmfbdq
zirocl (29)
jonshpm (99)
zmlth (154) -> zhxhkgf, cokzlht
bujroda (51)
bdvtvcu (74) -> tvcod, ouamzwh
jdrdxu (36)
troyu (29)
nrczsn (86)
aihow (92)
gaihmf (84)
ehjooz (124) -> hgwsl, mefxonk
omydd (6)
raevpsw (64)
aylmbfh (188) -> ddspu, thdwfw, kxnkbs, rziezq, jfjemon
diomq (65)
jjyjrtr (87) -> fjduphn, yjvgwdl
zsiziaa (38)
lyptirp (8)
lctdjj (56)
pbtks (85)
jxhrar (227) -> barnhza, iqovqp
neqfzm (13)
dhwauy (48)
qvjqfi (80)
ivstcsm (72)
aabrjf (72)
jvccsp (86) -> gukuqw, hpmbkwb
ddspu (113) -> yjmbbu, dzbrgb
zgevpxx (48)
qrrey (588) -> bhvmgw, wgexpa, xiotwdk
ncodn (62)
rbcqgqv (75) -> imcczga, xzurwza
fpxtub (11)
ldfopw (30)
ewyzqg (49)
iuhlc (6)
oqphsw (2722) -> iueejt, ekdqf, btbxk, jdshuob
eysrnaa (71)
ojsjuts (176) -> njxyw, dzasw, rpzaqc
ozyexx (83)
nnldikq (316) -> upwlxnb, vbxmpc, dgwcz
tfmtk (69)
hwctdr (76)
rothisa (66)
qnbfk (91)
qcgxvx (99)
igyiie (237) -> knirl, trbzi, auxvur, rvhxik
cverrt (52)
orrutjs (93)
ffloi (25) -> kflize, icgwppo
phrxnli (21)
eopxpo (41)
vlfouc (62)
fdnom (87)
wuxhvnx (86) -> ikfpktb, zcvipz
flefy (38)
yoeau (206) -> rfwgtb, drmyco
ozatmpe (34)
ydbri (66)
tufds (42)
pprhx (57) -> xitzb, zqyua, dtpexjq, zyradhz
zhxhkgf (29)
qwzmv (52)
paxzd (53)
cyzkk (60)
gyjxkl (37)
pzpjw (54)
svayf (89)
xxxqpkx (7)
imihjj (69) -> yygqky, qlkslp
tkpvf (47)
tljdqy (81) -> sxllorg, yatfpqx, zbznuyf, kymhbse, rfmeug, tetmzw
iphzyj (260) -> omsroa, mxupea
xiotwdk (177) -> jlnyr, nsqqw
eyyzy (274) -> opuaau, qolnvo, jxhrar
baewpe (55) -> svkdyq, hitoud, zvnxfa, emfctr, facrq, vykqcnj, bckuyxm
barnhza (20)
oafnfo (51)
pjcttzo (50)
aooni (205) -> xrvbzya, gvjrx
scchi (48)
zcgrnt (73)
pmsdv (93) -> pyypotx, marzlxh, zvepqr
kngbqid (89)
iwhqlr (949) -> ztkgsyt, ffloi, hzgig
vyxfljc (92) -> pyrlph, wdsiq, eysrnaa
hddzn (69)
cxvqvjz (136) -> kfrti, nslettz
tcospq (96) -> aabrjf, dllgpye
mnmwzz (142)
xfblj (40)
vfwegiu (46)
iphncut (138) -> wslsg, qhnaxuy
algqhtz (37) -> qeojk, sybpano
dmoxr (73)
tozktyo (29)
npjxq (46)
uvfyo (675) -> lxlbt, gnjvf, nfsuzef, spwgm
ollhxuy (821) -> vefzbc, faecnr, geldsqv, xneoi, cxvqvjz, jgkvfa, xtwdx
ksvfdcc (72)
avycyh (180) -> hwosyg, alqim
nsqqw (16)
nsfsj (99)
tpphe (64887) -> yatbsip, syzlt, uttujj
miwoup (40) -> gyjpoco, apgjv, eknui
iljwgzf (92)
bfuywyg (82)
aaqdb (44)
fgbyre (11)
kywfqzv (41) -> lajidkr, gyjxkl, wfhyr, evhsybt
aiovxpk (95) -> yoxvx, pbtks
hrovawq (50)
ajenoz (48)
aeuub (53)
gxjvj (163) -> yiusa, nrczsn
ippzix (9)
ttllx (73)
rorqy (43)
dqash (96)
lwvnbzs (24)
ckheb (34)
rgfndsx (18) -> qkbnq, welll, bkextqn, wnotwt
rsazi (62)
rpfmi (52)
uxslfay (72)
aemgsa (40)
jfmnsqg (85)
ggnsa (114) -> xhmfmo, azdei
lndaa (175) -> qvjqfi, iyuuh
kjdoubx (128) -> eopxpo, igyxt
dzasw (47)
emfctr (9120) -> qzckx, fsaoa, bjrpalu, mdneq, tdwtlf, hswrbpz, knltna
srqntb (137) -> raevpsw, qvteg
wweusm (66)
hawsl (13)
cupsjm (146) -> baiaa, pcqyagx
ppqlc (42)
tadnt (47) -> ufefj, rwxggm, rorqy
rvhxik (11)
vijkx (32)
lqcar (71)
dhkahb (49)
ftuemb (19)
ewdqb (50)
npmwcx (93)
wwezydn (97)
fuvru (98)
cdpwklz (83)
dtscjna (46)
exuusj (7)
ouamzwh (88)
ggvbqrp (145) -> opohwq, yrmgc, gewgn
ekdqf (467) -> ugvqayz, ysgsry, ogbsm
torxqh (90) -> dzwol, lepja
hpmbkwb (69)
ripqyzr (48)
eiklbh (32)
omdlwm (168) -> ihtnbb, hjjkx, bomho
lbwzat (74) -> iivncbz, dmoxr
pyypotx (51)
bjabd (7)
auzbdlz (95)
sxfilp (72) -> livlj, lgenxz
kxvlprg (60)
rfmeug (121) -> apygt, viwns, chtlcwq, wekkbw
xajjyba (164)
kzltfq (94288) -> vnrmx, lrihy, arqoys, nsmoh
mbhld (73)
rwxggm (43)
vapwxei (61)
ufefj (43)
oajawn (34)
dgnjf (335) -> yxseri, nscbsob
xaoncma (296) -> yipzce, nrpxx, rrfbngi
kqlsniq (95) -> qwsxpnc, mqmbcl, gtbbuvb
jrvbacq (49)
oavluo (21)
qpldch (54)
ieusgd (295)
tifgptk (100) -> ddldgex, ggvbqrp, focqhgt, cncak, ksvpnt, weuwc
lhradm (583) -> vusxa, lbwzat, ucbbun
apgjv (85)
cbibo (99)
jxhngrl (48)
qwsxpnc (96)
ysbrui (1293) -> iqggu, upvhfmn, kpqyb, wdeuy
ekvall (209) -> jxhngrl, aplvqql, drwfop
mkwfj (35)
pjiqvd (87)
pgubexv (78)
vbhnmr (2850) -> iftfc, kunzpa, qrrey, tljdqy
sjwhig (93)
zyradhz (52)
wcexum (116) -> eiklbh, vijkx
cdcye (53) -> izppmg, rxvyqsp
bdinafh (10)
rziezq (145) -> taiho, pkfhp
nslettz (10)
svhbd (109) -> xcvxle, fqzsq, jopjvd
limljj (68)
kauphp (231) -> dyxsmz, yzxzo
caryo (7)
nahovfk (109) -> flefy, cfztpc
qolnvo (267)
cmqwplb (9)
cfhuce (71) -> cecsr, josdslh
zwnvqu (88)
mhjtjp (91)
apkwi (222) -> rxragg, zsxizw
ioywk (16) -> ozyexx, eikmns, ktjav
yrmgc (31)
kqzemkv (96)
rxvyqsp (60)
hnlgkv (17)
raryuo (73)
bomho (87)
rixnft (85) -> cpndnx, fpxtub
zoewj (193) -> ohbuhy, ymckwqo
hnyqq (34)
tkmed (1959) -> tuqmup, jwgchxu, sjforw, zmsosb, tqikxkp
wlpyulp (10)
pixjzh (158) -> fgjwz, lsknlg, hlcghe, txhfuoh, hdvel
likvlm (62)
xhmfmo (48)
rgrxpe (69)
weuwc (84) -> xtwdau, muncur
uevcwul (92)
kpxqlr (155) -> nbbyqsa, ilkqp
fqzsq (98) -> tiujei, yhubw
ubovv (6)
knirl (11)
lzvniiz (60)
cwtdf (29)
qeojk (99)
ycxzfkf (131) -> bgflw, chophr
thjulip (20)
vgdwm (53)
myhch (25)
bovno (175)
uqlso (48)
rhnkdt (59) -> rsazi, ncodn, pwizhzr, likvlm
acpfsnb (204) -> nmlcne, vfsttaj
wzfkk (99)
oqlpz (81)
nscbsob (24)
mzmfygf (171) -> jxyoypa, ippzix
rvrlma (211)
pfphng (90)
mdiqsgg (12)
jtzkva (274) -> flomey, ukvvt
tvwxmur (64) -> yodoqn, ksvfdcc, ivstcsm, pvgzz
aplvqql (48)
qybmgto (9)
mtcrswx (75)
aphpzub (29)
vchsdif (105) -> ofisj, zwnvqu
dllgpye (72)
lfzahrm (79)
oiosol (27)
geldsqv (80) -> ienye, eeppf, ftuemb, vbbgeo
vlbba (81) -> ewdqb, vfzby, pjcttzo, abddskq
nfsuzef (75) -> dlbzng, cbibo, wzfkk, jonshpm
lryzkx (71)
mhndszl (190) -> tbrfk, xprzeeb
jbepak (66)
nmlcne (27)
gfffvbp (8)
bqtas (93)
fhmauag (221) -> vantwg, kzwqzqf, vfwegiu
misyfn (82) -> uixlx, oupzsh, bovno
jtauf (13) -> xskehl, bmfhjm, srhirm, kjfmqkt, qzxaqvy
eerktn (85) -> npjxq, kasfuwe, ljbss, theau
ktaet (58)
eeppf (19)
vgqeyx (31)
qhnaxuy (31)
xrvbzya (35)
nzqcq (66) -> vewgrvp, vfngjd, sjrxs, hvjtn, ecokyy, gcaxntb, omdlwm
sybpano (99)
ebsniof (39)
urzul (9)
srmiagk (292) -> dvdgowj, vqpeg, gjuekv
uexdnv (82)
pgspysb (40)
wymfopy (93)
nqhdt (164) -> mkwfj, gjwaqu, sxmbcwp
twzpqip (41)
bniti (66)
yfjenp (295) -> qxfce, zsiziaa
meoeea (60) -> laczal, tcvabyz
heacb (53)
focqhgt (238)
dtstgj (36)
kkmqko (7)
vcjjo (98)
nnnkeh (445) -> gzzpja, bhuyfk, xnukvni, tttle, snzfrer
baesyhf (1013) -> tznkwk, hcjxz
hygfoe (85)
wtxbqe (87)
vwzglf (58)
hswrbpz (254) -> flcqsb, sbguah, cdcye
axtqrx (29)
auxvur (11)
iqggu (444)
kceusl (42)
jykbb (91)
nxzkuj (75)
xzurwza (95)
rrflox (52)
kfmzbvk (10)
mnkwo (212) -> jyskb, wfphcf
dfvhic (82) -> fhmazv, hwctdr
gfzbp (197) -> ymcuygn, mxzbcqn
tlednk (39)
lgenxz (54)
emwbbut (9)
exoft (17)
woolxv (49)
auxqbbc (87)
wvocz (67)
hvjtn (325) -> cverrt, kfxoi
aunhcg (613) -> kjdoubx, ggnsa, acknlp
absdwf (39)
wajnxjj (40) -> imjzf, wwezydn
hgdbaol (10)
cfztpc (38)
chlxm (46)
ljbss (46)
gauumxf (230) -> tkiraal, lyptirp
nhlittn (22)
gcaxntb (405) -> mdiqsgg, oxiuaz
lfxew (66)
bamxg (66)
wdsiq (71)
mykrcq (98) -> zcgrnt, raryuo, okrdziq
erpvue (91)
kmwbbz (93)
vsgaam (7)
hokyk (66)
pjzpmq (38)
iqovqp (20)
mmcychg (65)
guncf (259) -> proshun, wxjka
jatnl (216) -> oavluo, phrxnli
nhkvp (100) -> rgrxpe, nscav, illjvf
hcjxz (31)
mqrroj (243) -> jtjcj, dnmvzeg
lvksghj (18)
mhsjkm (84)
popplum (89)
vusxa (30) -> ieadjz, mzmtuw
dmkbnot (26)
httit (18)
tbrfk (19)
ztzwh (48)
imjzf (97)
rypdxr (105) -> qyoqb, lejgcu, djirpp
qzckx (35) -> qzzkvf, pmsdv, gauumxf
xbnmvd (76)
ouymke (47)
rajtef (365) -> iriun, ezaypy
itngcua (65)
orxoo (66)
tcdwurt (18)
auqoj (99)
sqnvvbg (36)
rxragg (18)
kpqyb (258) -> sqkcdf, iqxwh, vnhvilk
proshun (47)
uscufoy (15)
tpipb (61)
owhjmt (155) -> vsruoi, ifxcrug
bkvle (9)
yosnw (32) -> ilymgq, yppydul, yamclb
iynywq (66)
nxpexoq (92)
eviqjr (25)
trbzi (11)
rfvomn (95)
ohbuhy (41)
vkpltts (73)
ktpte (9)
bbgwzg (79)
bgcigo (8) -> bruzfkf, lxcbjgy, vlmcmcu
ecokyy (357) -> iaphzk, httit, vztnh, owmni
jwgchxu (32) -> rfvomn, auzbdlz
xlskkfi (92)
uxjasn (36)
dcumfo (73)
wpnqet (87)
ilqol (88)
bhsbd (53)
flcqsb (115) -> meypo, aphpzub
yvqtyi (85)
oyvhouc (37) -> cdpgoi, bbgwzg, xoziel, lfzahrm
bjhickt (23)
hmvwl (32) -> nswximo, tpphe, baewpe, hghnmib, kzltfq
oiijtm (20)
ylfsnz (93)
imynb (146) -> absdwf, cikaze
yygqky (82)
yuswp (68)
izppmg (60)
itwbpot (22)
hwosyg (42)
mkrzp (211) -> laxsl, zirocl
vqpeg (5)
gddkqw (244) -> vhtyadn, lvksghj
bhuyfk (79) -> aghdlll, ilqol
yrfqaga (103) -> jqinti, zjaklmn
bnfopv (118) -> cjmxed, zlzers, qrlggma
welll (99)
ehuzoq (77)
nqyok (77)
rrfbngi (21)
yoezrpw (38)
rpzaqc (47)
qxlucvg (84)
tehyhc (13)
gqrfok (231) -> kfhnhm, aituccf, qrkhol
zvnxfa (10022) -> aylmbfh, lwencl, pixjzh
gzzpja (255)
ofrwmq (205) -> iigvpqy, wweusm
qanbo (50)
obslyn (13)
hwovhvw (915) -> qdhrchr, nahovfk, xomnhw, ycxzfkf
smlfbc (1615) -> wnjwnr, pprhx, aiovxpk
xbkeua (157) -> pgspysb, aemgsa, xfblj, hswzo
btklib (51)
owmni (18)
qzzkvf (108) -> aobitc, tsrogy
umtrod (22)
vxajmkg (71)
jmlmzpz (62)
plurwe (228)
jyskb (6)
xnuoujm (16)
nakmo (10)
uzhlers (50)
umlkxqv (20) -> ecimj, wudjf, jfmnsqg
ziqwzzy (204) -> uscufoy, fooyrq
ymrogz (272) -> ebsniof, tlednk
lpuass (28)
qrkhol (9)
hpkpw (38)
gtzcxq (73)
gvjrx (35)
ieadjz (95)
tcukgv (66)
ifxcrug (55)
thxtoc (178) -> trtgn, fdnom
puwvse (414)
pvppi (246) -> qlwxeb, nuqyqh
vcixs (260) -> noipcz, frohei
cichyqw (71)
ugvqayz (126) -> xfekjt, wvocz
hrqzqqh (53)
qedst (18)
wnjtb (73)
kjfmqkt (138) -> pzpjw, qpldch
ussmw (94)
sxmbcwp (35)
dqdfv (73)
ptyxo (13)
upuxd (36)
fppcif (209) -> uxslfay, yjhes
kxykfr (82) -> twzpqip, qymwy
yodoqn (72)
mnzbkuh (28) -> jtouvtb, wdvwub
omdpc (26)
ccrftvw (62)
bmfhjm (222) -> lyvyhkm, sbyxyf, kblshw
fwgqj (1924) -> zmcgfdp, vzuqbye, rypdxr
rlbom (79)
livlj (54)
ybvgki (8)
zcvipz (97)
xyohoxa (928) -> qkkzzlm, lmuyfcw, avycyh
dchts (99) -> lctdjj, oevyknd
ksfok (217) -> gfffvbp, ybvgki
hoomyh (88) -> aaqdb, ljfqvk
qijarlh (58)
tznudmk (17)
cyrrjtx (124) -> oqbdf, xwlmsqy, ulztj, rjsnth
nuqyqh (52)
oblsboq (85)
imnhql (94)
hxswghs (126) -> dwwsu, hdlqvlg, jppgd
ulztj (25)
hgwsl (50)
ksvpnt (96) -> fqlezvk, lqcar
mjpzp (10)
fsaoa (89) -> dbwmq, uzufet, arwmalf, gobrf
iftfc (159) -> thxtoc, jtzkva, tvwxmur
zjpsm (83)
vwfhi (9)
opuaau (75) -> dqash, kqzemkv
mxupea (45)
dmkyzy (15) -> ttllx, horqcc, dcumfo
sxllorg (69) -> kxvlprg, lzvniiz
txhfuoh (219) -> lwdqnj, myhch
chtlcwq (17)
hlcbqu (104) -> ccrftvw, jmlmzpz
ivmndi (94)
lficpr (62)
ortqc (99)
dvzlq (33)
acknlp (56) -> aozoac, ehuzoq
jqxnf (60)
hfftu (52)
ihzvygq (94) -> kmwbbz, orrutjs
rarkunn (73)
hitoud (5511) -> vcktg, rqbjbio, xtyzy, ssdgbnh
sdhtguj (58) -> uklsrym, mcmqliy, nnnkeh, clinrg, fwidkbp, hzmhm, xyohoxa
hrlkgen (99)
vuyzhsh (61)
nzzfer (85) -> qcgxvx, ortqc, auqoj, ilfzi
tuqmup (222)
zbznuyf (137) -> ptyxo, qwtzc, neqfzm, hawsl
qwtzc (13)
vykqcnj (71) -> jitzj, nkhadt, tcsbho, fhxpkd, fwgqj, smlfbc
mjzksjz (7)
yfdtz (36)
faixe (56)
tejnuve (209) -> jgmisxl, dhkahb
opohwq (31)
lsknlg (95) -> vwzglf, hjucki, yrkvb
fhmazv (76)
egmfbdq (25)
rxcnn (9)
tboizos (250)
glwhd (122) -> ceoav, troyu
ykehxw (19)
bruzfkf (91)
rjjlus (87)
ocnna (18)
qshbt (73)
raakduh (85) -> fuvru, vcjjo
wudjf (85)
ihwaeuw (60)
kfxoi (52)
oewzluz (39)
coopirx (251) -> exuusj, rvimq
cokzlht (29)
uacjhqx (23)
tznkwk (31)
mthhq (111) -> uevcwul, nxpexoq
uixlx (7) -> kmlwj, gaihmf
nqvxs (71)
ktjav (83)
eknui (85)
fhuiyrl (93)
fktsu (65)
vugnug (65)
ilymgq (91)
clinrg (1033) -> rsancy, jrqorlo, lvklj
bkextqn (99)
ekohgo (251) -> xxxqpkx, wkphn
alkneau (34)
mnijdlk (85)
dyxsmz (38)
mefxonk (50)
lajidkr (37)
uiuokpq (89)
oupzsh (43) -> bzmade, bamxg
cijptz (18)
khibjj (89)
yamclb (91)
okrdziq (73)
sbyxyf (8)
zknziw (18)
fobzai (75)
rjsnth (25)
iaphzk (18)
lufgosn (10)
rzkcu (34)
xlhfyw (471) -> yuswp, limljj
tcsbho (1842) -> mnmwzz, mnzbkuh, zpidc, cpqti
docln (85)
neeqb (7)
tvcod (88)
uklsrym (40) -> bbhniy, gddkqw, lhmnd, ihzvygq, nhkeb, wuxhvnx
qkkzzlm (76) -> imnhql, nbeagw
qywkuqu (20)
fvgbg (191) -> iwkntdi, jdrdxu, sqnvvbg, yfdtz
qlkslp (82)
iqxwh (62)
mdneq (623) -> uzhlers, qanbo, tedplb
msmgk (173) -> fygmpjn, exoft
euoclfs (241) -> pjzpmq, hpkpw
vlimzz (19) -> yvqtyi, gwournc, docln, oblsboq
zoqni (189) -> chlxm, yfmxvay
oignan (206) -> hdaqxlh, fgbyre
zpidc (40) -> bujroda, btklib
aazxafl (215) -> xnmvtem, oafnfo
yhubw (34)
xneoi (138) -> vwfhi, cmqwplb
vefzbc (138) -> dywqvqh, emwbbut
ruozmjk (73)
jrwfehi (75) -> kcnim, bdvtvcu, tfsoxgb, tboizos
iivncbz (73)
ccuarv (53)
lrihy (185) -> vchsdif, bgcigo, raakduh, vlbba, igyiie, zoqni
vewgrvp (73) -> dntphko, svayf, uiuokpq, popplum
iigvpqy (66)
fjduphn (91)
uttujj (11755) -> glwhd, sxfilp, wcexum
tluap (6)
exeub (71)
dzwol (61)
ilfzi (99)
cdpgoi (79)
hxckb (71)
yoxvx (85)
theau (46)
vwnjh (233) -> jqxnf, qfpwln
jbpjt (27)
zmsosb (14) -> rrflox, ovluts, rpfmi, ojvlwm
yoivja (59)
towlhi (36)
zcrjb (253) -> qhohy, uwaiki
josdslh (59)
xoziel (79)
fsuzqyz (169) -> duftj, ppqlc, kceusl
chwjiub (96)
fpbsu (89)
qyoqb (19)
dfeomzr (38)
kfhnhm (9)
oevyknd (56)
buoakk (22)
wduqgix (77)
qokscr (65)
oqbdf (25)
jjsvfy (199) -> yoivja, gdnsat
ssdgbnh (887) -> qtsjbq, plurwe, mhndszl, hlcbqu, pgskth, oignan
lrsedv (213) -> eaqjcju, cekpxgj
iwkntdi (36)
qfgzmtz (73)
rfwgtb (26)
alcvj (7)
bvdxf (30)
ofisj (88)
mpchqe (27)
pwizhzr (62)
wkcyd (75)
mxzbcqn (81)
npzdqeg (227) -> tufds, msxhvo, pcsucog
illjvf (69)
iyuuh (80)
fygmpjn (17)
dvdgowj (5)
hlcghe (91) -> khibjj, kngbqid
zvurtb (77)
ouspx (46)
dbvxai (76)
facrq (13496) -> fkbla, ffvprc, yrfqaga, msmgk, hxswghs
xbcgipi (66)
wfhyr (37)
ziyata (221) -> oqlpz, jjtrisl
muncur (77)
vlvss (183) -> odvtiti, fazqw
kvdkwy (96)
ddldgex (84) -> nqyok, wduqgix
trtgn (87)
jitzj (65) -> fvgbg, nbfqgr, zjwpbzs, lndaa, vlvss, gxjvj, zcrjb
hkhoyje (95) -> frirj, iuhlc
gtbbuvb (96)
tfsoxgb (250)
rohvy (95)
qhohy (41)
goimlra (227) -> orxoo, lfxew
hubbqbi (95)
vchuc (53)
svkdyq (9559) -> akmgfo, lhradm, jtauf, aunhcg
fazqw (76)
flomey (39)
apygt (17)
wjptb (43)
srhirm (147) -> bicsjoc, dvzlq, olykwbi
wdeuy (254) -> hubbqbi, rohvy
yeooycn (93)
qoyzgsp (28)
sqkcdf (62)
rgbvlc (49)
qinzaf (813) -> aooni, zoewj, ogzrdrk, umlkxqv
kflize (84)
isrtfc (201) -> vmutyru, ouymke
nkhadt (292) -> fppcif, vwnjh, oyvhouc, ekvall, guncf, npzdqeg
nbbyqsa (40)
ikfpktb (97)
maqgick (76)
xtwdx (156)
sbyzsq (10)
vgubuy (74) -> iljwgzf, aihow
taiho (59)
cpndnx (11)
vhtyadn (18)
aaheijb (54)
rykadr (19)
onnylx (32)
gukuqw (69)
fooyrq (15)
zqyua (52)
vsruoi (55)
ikmvhid (2745) -> hwovhvw, arsuc, yzrdupu
vztnh (18)
khaupo (32)
cpqti (142)
qtsjbq (126) -> wekya, rzkcu, alkneau
pcsucog (42)
lepja (61)
ibjvonk (10277) -> xlhfyw, svhbd, misyfn
rqbjbio (29) -> mqrroj, hjeysaa, wlujpl, vooac, rrggg, yfjenp
ceuygh (90) -> aqxsjq, qxlucvg
qzxaqvy (78) -> fwskxtt, jlgvplm
fwskxtt (84)
yrkvb (58)
thdwfw (219) -> umtrod, nhlittn
zpkbe (73) -> cwtdf, tozktyo, qcrpdy, axtqrx
hjjkx (87)
jxyoypa (9)
ilkqp (40)
akwvj (238) -> jatnl, iphgmyt, meoeea, gqrfok, ljhwzvv
lkcddrg (2238) -> lqfyzo, rixnft, hkhoyje
xprzeeb (19)
rhodopg (94) -> qfgzmtz, dqdfv
ttwfig (340) -> rykadr, ykehxw
kueyf (85) -> ulbbc, nzzfer, azxjd
zmcgfdp (136) -> tehyhc, obslyn
ffnabs (20) -> guehoas, nnldikq, ofrwmq, lrsedv, qvkotfd, shfdaba
arwmalf (143) -> vsgaam, bjabd, ycclns, kkmqko
gyjpoco (85)
drmyco (26)
arqoys (1859) -> urzul, bkvle
nscav (69)
tsrogy (69)
qhafxnl (1337) -> xbcskih, kpxqlr, algqhtz
yiusa (86)
zdbqs (43)
xzppxad (58) -> ltxkw, ollhxuy, qinzaf, wpxxh
dxyifeb (1862) -> twubx, lkcddrg, uwqgz, uvfyo
zlzers (49)
gkkgkp (358) -> wlpyulp, nakmo
abddskq (50)
tggkm (43)
dgwcz (7)
bhvmgw (29) -> qflouyn, pfphng
guehoas (283) -> qedst, cijptz, zknziw
marzlxh (51)
mizab (60)
jgkvfa (120) -> ocnna, tcdwurt
jopjvd (80) -> dnouufu, wjptb
lwdqnj (25)
xpzhy (84)
noipcz (59)
bbhniy (20) -> itngcua, mmcychg, vugnug, fktsu
jtjcj (64)
tgdzl (53)
gobrf (25) -> gtzcxq, lsdrwz
arsuc (65) -> rbcqgqv, huwsoc, bnfopv, srqntb, vxdkej, owhjmt
ogzrdrk (101) -> vztbn, wtxbqe
oxbkwyr (91)
yatfpqx (109) -> xrbjn, qywkuqu, thjulip, oiijtm
jlgvplm (84)
bcibchp (54)
glgnecl (16)
tqikxkp (222)
bhcal (7)
vmutyru (47)
kzwqzqf (46)
evhsybt (37)
gdnsat (59)
cikaze (39)
jrqorlo (229)
ovluts (52)
nbfqgr (169) -> cdpwklz, zjpsm
nbngkou (73)
wslsg (31)
aobitc (69)
htgxu (24)
wjolzt (46)
hzgig (95) -> jrvbacq, rgbvlc
ulbbc (217) -> bniti, jbepak, iynywq, xbcgipi
wkphn (7)
fkbla (207)
jqinti (52)
yhiogu (256) -> neusnw, tkpvf
ebjsluk (39)
shfdaba (76) -> wpnqet, rjjlus, pjiqvd
anpnrdt (10)
jdshuob (491) -> kywfqzv, zpkbe, cfhuce, mzmfygf
vooac (341) -> lufgosn, sbyzsq, mjpzp
frohei (59)
baiaa (15)
pyrlph (71)
cgxsmq (25)
ukvvt (39)
gaujsyk (26) -> ktaet, yipoeia, qijarlh
gnjvf (375) -> ajenoz, ripqyzr
hghnmib (47802) -> vbhnmr, vustse, lybkeg, ikmvhid, oqphsw, xzppxad, gvkcsad
yrcgsnx (270) -> qfypnb, dbvxai
kwqrbav (34)
wdvwub (57)
viqhfi (89)
akmgfo (243) -> zhvji, iphncut, oyxbblb, gaujsyk, ybftt
faecnr (80) -> dfeomzr, yoezrpw
xskehl (228) -> ubovv, omydd, tluap
pdosfg (21) -> rlbom, lbjwlov, wgqkdcr
tkiraal (8)
aimav (46)
ecimj (85)
eikmns (83)
fqlezvk (71)
qrlggma (49)
ztkgsyt (29) -> bfuywyg, uexdnv
tedplb (50)
cvrcvgp (86) -> zvurtb, dkcix
bckuyxm (11306) -> eyyzy, jrwfehi, baesyhf
ffvprc (65) -> vxajmkg, cichyqw
jjtrisl (81)
vantwg (46)
vlmcmcu (91)
qdhrchr (89) -> dhwauy, uqlso
ceoav (29)
bhrbod (50) -> oxbkwyr, erpvue, zhrnwk, mhjtjp
yxseri (24)
kzbvrxk (10)
kcnim (76) -> zjoxibi, auxqbbc
ltxkw (30) -> eerktn, nqhdt, jjyjrtr, bfchbs, redqvw, mkrzp, nymguj
rrggg (371)
uwqgz (1923) -> torxqh, zmlth, lnctft
dbwmq (117) -> bmecxwd, lcrwbqi
kasfuwe (46)
btbxk (755) -> xajjyba, kxykfr, rymkqd
njxyw (47)
fvlfq (94)
zhvji (162) -> cpazlc, mluykm
aozoac (77)
chnkkj (86) -> tfmtk, hddzn
dkcix (77)
lxcbjgy (91)
mofks (30)
yzrdupu (719) -> wajnxjj, dfvhic, dmkyzy, ziqwzzy
wxjka (47)
xitzb (52)
rvimq (7)
qddsx (30)
lvklj (97) -> ydbri, tcukgv
sjforw (208) -> alcvj, neeqb
yjvgwdl (91)
fhxpkd (261) -> kauphp, zdhvqrl, rhnkdt, nhkvp, tejnuve, olspit, srmiagk
eaqjcju (62)
ybftt (122) -> oewzluz, ebjsluk
jgmisxl (49)
hdaqxlh (11)
cjmxed (49)
aqxsjq (84)
cekpxgj (62)
tetmzw (121) -> ozatmpe, qbmtmcs
mqmbcl (96)
xtyzy (155) -> yhiogu, iphzyj, pvppi, tojyt, krxyaak, ymrogz
drwfop (48)
pgskth (86) -> hxckb, lxesg
pvgzz (72)
kunzpa (687) -> tadnt, cupsjm, hoomyh
nhkeb (252) -> caryo, bhcal, mjzksjz, ufitse
cncak (182) -> qoyzgsp, lpuass
aituccf (9)
qfpwln (60)
laxsl (29)
yzxzo (38)
lnctft (116) -> zgevpxx, scchi
lyvyhkm (8)
vcktg (1556) -> ztghd, imihjj, ksfok
dzbrgb (75)
xbcskih (85) -> fobzai, nxzkuj
jtouvtb (57)
ufitse (7)
upwlxnb (7)
jysaup (78)
ysgsry (228) -> glgnecl, xnuoujm
horqcc (73)
vfsttaj (27)
gvkcsad (5412) -> ghsjtj, dgnjf, ziyata, rajtef, kqlsniq, vqclii
lbjwlov (79)
vnhvilk (62)
dntphko (89)
syzlt (6183) -> tifgptk, iwhqlr, akwvj, kueyf
hzmhm (1087) -> rvrlma, dchts, emzrj
neusnw (47)
vfzby (50)
cecsr (59)
uwaiki (41)
msxhvo (42)
fgjwz (113) -> qwzmv, xehdglb, kgpwo
lmuyfcw (164) -> hrovawq, hacwv
zjoxibi (87)
viwns (17)
olykwbi (33)
meypo (29)
sbguah (49) -> vlfouc, lficpr
oyxbblb (92) -> towlhi, fndxl, uxjasn
bzmade (66)
lfpzff (238) -> bdinafh, kfmzbvk
epuaii (88) -> ckheb, kwqrbav
dwwsu (27)
xnukvni (207) -> htgxu, lwvnbzs
zhrnwk (91)
vfngjd (325) -> hfftu, nymhem
vztbn (87)
kxnkbs (19) -> tpipb, vuyzhsh, vapwxei, wbxdta
bmecxwd (27)
nymguj (123) -> vkpltts, mbhld
qlwxeb (52)
kfrti (10)
xcvxle (106) -> qddsx, bvdxf
wbesqn (99)
kblshw (8)
qymwy (41)
ezaypy (9)
dnouufu (43)
cyapi (227) -> rothisa, hokyk
itbsk (30)
alqim (42)
hjeysaa (251) -> mofks, itbsk, njogewi, ldfopw
ljfqvk (44)
iueejt (5) -> rgfndsx, bhrbod, puwvse
knzppj (81) -> hrlkgen, nsfsj, wbesqn
wnjwnr (197) -> hnyqq, oajawn
xtwdau (77)
dmeee (93)
qxfce (38)
pcqyagx (15)
bicsjoc (33)
eeguu (78)
wbxdta (61)
gjwaqu (35)
mzmtuw (95)
huwsoc (173) -> ouspx, wjolzt
spdhhoe (167) -> chwjiub, kvdkwy
hhmwlo (56)
icgwppo (84)'''


if __name__ == "__main__":
    unittest.main()
