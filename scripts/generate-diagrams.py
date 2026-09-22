from pathlib import Path
from html import escape
out=Path(__file__).resolve().parents[1] / 'public' / 'diagrams'
out.mkdir(parents=True,exist_ok=True)
INK='#205c48';GRAY='#64786b';ACC='#bb743c'
def text(x,y,s,size=17,color=INK,anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>'
def line(x1,y1,x2,y2,extra=''):
 return f'<path d="M{x1} {y1}L{x2} {y2}" {extra}/>'
def path(d,extra=''):return f'<path d="{d}" {extra}/>'
def dot(x,y):return f'<circle cx="{x}" cy="{y}" r="4" fill="{INK}"/>'
def gnd(x,y):return path(f'M{x} {y}v10m-17 0h34m-28 7h22m-16 7h10')
def rh(x1,x2,y,label=''):
 mid=(x1+x2)/2
 return line(x1,y,mid-25,y)+f'<rect x="{mid-25}" y="{y-10}" width="50" height="20"/>'+line(mid+25,y,x2,y)+(text(mid,y-23,label,16,anchor='middle') if label else '')
def rv(x,y1,y2,label=''):
 mid=(y1+y2)/2
 return line(x,y1,x,mid-22)+f'<rect x="{x-10}" y="{mid-22}" width="20" height="44"/>'+line(x,mid+22,x,y2)+(text(x+23,mid+5,label,16) if label else '')
def cv(x,y1,y2,label=''):
 mid=(y1+y2)/2
 return path(f'M{x} {y1}V{mid-6}m-20 0h40m-40 12h40m-20 0V{y2}')+(text(x+27,mid+5,label,16) if label else '')
def ch(x1,x2,y,label=''):
 mid=(x1+x2)/2
 return path(f'M{x1} {y}H{mid-6}m0-20v40m12-40v40m0-20H{x2}')+(text(mid,y-29,label,16,anchor='middle') if label else '')
def diode(x,y,led=False):
 s=path(f'M{x-35} {y}H{x-15}M{x-15} {y-16}L{x+12} {y}L{x-15} {y+16}ZM{x+12} {y-20}V{y+20}M{x+12} {y}H{x+35}')
 if led:s+=path(f'M{x+3} {y-22}l17-16m-8 0h8v8M{x+19} {y-10}l17-16m-8 0h8v8')
 return s
# text isn't stroked

def save(name,title,body):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 350" width="720" height="350" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7z" fill="{INK}" stroke="none"/></marker></defs><rect width="720" height="350" fill="#f1f6f2" rx="7"/><g stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none">{body}</g><style>text{{stroke:none;font-family:'Noto Sans JP',sans-serif}}.caption{{fill:{GRAY}}}</style></svg>'''
 (out/(name+'.svg')).write_text(svg)

b=text(30,33,'LED点灯回路',19)+text(35,137,'＋5 V')+line(70,155,105,155)+rh(105,245,155,'R1 620 Ω')+line(245,155,320,155)+diode(355,155,True)+line(390,155,555,155)+line(555,155,555,220)+gnd(555,220)+text(315,205,'A')+text(372,205,'K')+text(326,106,'D1 LED')+text(490,277,'GND / 0 V')+path('M118 235h130','marker-end="url(#arrow)"')+text(126,267,'I ≈ 4.84 mA',16)+text(30,320,'電流は＋電源 → 抵抗 → LED → GND → 電源−へ戻る',15,GRAY)
save('led','LEDと620Ω抵抗の直列回路',b)
b=text(30,33,'分圧と電圧測定',19)+text(180,65,'Vin = 5 V')+rv(270,80,155,'R1 10 kΩ')+line(270,155,270,180)+dot(270,180)+rv(270,180,275,'R2 10 kΩ')+gnd(270,275)+line(270,180,535,180)+text(400,161,'Vout ≈ 2.5 V',16)+line(535,180,535,207)+f'<circle cx="535" cy="235" r="28"/>'+text(535,241,'V',20,anchor='middle')+line(535,263,535,285)+line(270,285,535,285)+text(577,239,'DMM',15)+text(35,322,'電圧計は出力とGNDの間へ。低抵抗の負荷をつなぐと分圧比が変わる。',14,GRAY)
save('divider','抵抗分圧と並列電圧計',b)
b=text(30,33,'ローパス：Cの両端を出力に',18)+text(383,33,'ハイパス：Rの両端を出力に',18)
b+=rh(40,220,120,'R')+line(220,120,310,120)+dot(245,120)+cv(245,120,230,'C')+gnd(245,230)+text(30,94,'Vin',15)+text(275,99,'Vout',15)+text(48,294,'遅い変化を通す',16)
b+=ch(390,570,120,'C')+line(570,120,670,120)+dot(600,120)+rv(600,120,230,'R')+gnd(600,230)+text(380,94,'Vin',15)+text(630,99,'Vout',15)+text(398,294,'速い変化を通す',16)+text(225,331,'fc = 1 / (2πRC)',19)
save('rc','RCローパスとハイパスの接続比較',b)
b=text(30,33,'スイッチ入力のプルアップ',19)+text(150,78,'＋3.3 V')+rv(215,90,185,'10 kΩ')+dot(215,185)+line(215,185,520,185)+text(470,163,'GPIO入力',17)+line(215,185,215,225)+dot(215,225)+line(215,225,240,263)+dot(215,275)+line(215,275,215,290)+gnd(215,290)+text(262,256,'SW',17)+text(370,249,'開：H（約3.3 V）',16)+text(370,282,'閉：L（約0 V）',16)
save('pull-up','プルアップ抵抗とGNDへ閉じるスイッチ',b)
b=text(30,30,'NPN 低側スイッチ',19)+text(472,55,'＋5 V',16)+rv(500,65,125,'620 Ω')+line(500,125,500,142)+path('M488 142h24l-12 21zM487 165h26M500 165v15')+path('M520 143l16-12m-7 0h7v7M525 157l16-12m-7 0h7v7')+text(558,158,'LED',15)
b+=line(500,180,500,198)+line(500,198,462,220)+line(462,210,462,266)+path('M462 248L500 275','marker-end="url(#arrow)"')+line(500,275,500,292)+gnd(500,292)+text(520,220,'C',16)+text(520,284,'E',16)+text(436,207,'B',16)+text(561,244,'Q1 NPN',17)
b+=text(34,210,'3.3 V制御',16)+rh(40,295,237,'RB 2.2 kΩ')+line(295,237,462,237)+dot(340,237)+rv(340,237,308,'100 kΩ')+gnd(340,308)+text(29,320,'制御源と負荷電源のGNDを共通にする',14,GRAY)
save('bjt','NPNトランジスタによるLED低側駆動',b)
def fetbase(title='MOSFET 低側スイッチ',load=True):
 b=text(25,30,title,19)+text(450,55,'＋5 V',16)
 if load:b+=rv(490,65,144,'負荷 1 kΩ')
 b+=line(490,144,490,176)+f'<rect x="425" y="176" width="130" height="89" rx="5"/>'+text(490,214,'N-MOSFET',16,anchor='middle')+text(490,240,'端子接続図',12,GRAY,anchor='middle')+text(501,171,'D',15)+text(404,215,'G',15)+text(504,282,'S',15)+line(490,265,490,295)+gnd(490,295)+rh(40,280,220,'RG 1 kΩ')+line(280,220,425,220)+text(35,185,'GPIO',16)+dot(310,220)+rv(310,220,300,'100 kΩ')+gnd(310,300)
 return b
save('mosfet','N-channel MOSFETの端子接続図',fetbase()+text(28,337,'G-S間のプルダウンでOFFを保持。図は抵抗負荷の例。',14,GRAY))
b=fetbase('リレーのコイル駆動と保護',False)+path('M490 65v9c-25 0-25 18 0 18c-25 0-25 18 0 18c-25 0-25 18 0 18v16')+text(335,103,'5 Vコイル',16)+line(490,65,630,65)+line(630,65,630,89)+path('M615 89h30M630 89l-15 27h30zM630 116v28')+line(490,144,630,144)+dot(490,65)+dot(490,144)+text(654,92,'K',15)+text(654,142,'A',15)+text(552,40,'フライバックD',13)+text(27,337,'Kを電源＋、Aをコイル下側へ。接点回路は省略。',14,GRAY)
save('relay','リレーコイルに並列な逆向きダイオードの接続',b)
b=text(25,30,'非反転増幅：Av = 1 + Rf/Rg',19)+path('M270 75L270 220L425 148z')+text(286,115,'＋',22)+text(286,195,'−',22)+line(60,108,270,108)+text(45,85,'Vin 0〜1 V',16)+line(425,148,635,148)+dot(520,148)+text(546,127,'Vout 0〜3 V',16)+line(520,148,520,255)+rh(235,520,255,'Rf 20 kΩ')+line(235,188,270,188)+line(235,188,235,255)+dot(235,255)+rh(75,235,255,'Rg 10 kΩ')+line(75,255,75,285)+gnd(75,285)+line(325,101,325,58)+text(339,64,'＋3.3 V',15)+line(325,194,325,216)+gnd(325,216)+text(315,325,'電源に100 nFを近接配置（図では省略）',14,GRAY)
save('opamp','負帰還を持つ非反転オペアンプ3倍増幅回路',b)
b=text(25,33,'電圧測定：並列',19)+text(390,33,'電流測定：直列',19)+text(35,75,'＋3 V',16)+line(80,86,80,110)+rh(80,285,110,'R 1 kΩ')+line(285,110,285,270)+gnd(285,270)+line(80,110,80,210)+line(80,210,156,210)+f'<circle cx="183" cy="210" r="27"/>'+text(183,216,'V',21,anchor='middle')+line(210,210,285,210)+dot(80,110)+dot(285,210)+text(55,313,'赤V/Ω・黒COM',15,GRAY)
b+=text(399,76,'＋3 V',16)+line(443,85,443,110)+line(443,110,481,110)+f'<circle cx="510" cy="110" r="29"/>'+text(510,117,'A',21,anchor='middle')+line(539,110,620,110)+rv(620,110,230,'R')+line(620,230,620,270)+gnd(620,270)+text(391,312,'赤は指定電流端子・黒COM',15,GRAY)+text(345,343,'接続を変えるときは電源OFF',14,ACC,anchor='middle')
save('measurement','電圧計は並列、電流計は直列',b)
b=text(25,30,'波形の基本',19)
for yy,lab in [(118,'正弦波'),(250,'矩形波')]:
 b+=text(25,yy,lab,17)+line(125,yy,670,yy)+line(125,yy+45,125,yy-55)+text(677,yy+7,'t',16)
b+=path('M130 118C160 38 190 38 220 118S280 198 310 118 370 38 400 118 460 198 490 118 550 38 580 118 640 198 670 118')
b+=path('M130 250h35v-50h90v50h90v-50h90v50h90v-50h90v50h55')+line(175,50,355,50)+line(175,43,175,57)+line(355,43,355,57)+text(258,41,'T',17,anchor='middle')+text(175,326,'f = 1/T　　Vpp = 最大値 − 最小値',18)
save('waveforms','正弦波と矩形波の周期と電圧',b)
b=text(25,30,'オシロ画面：電圧と時間',19)
for x in range(110,661,55):b+=line(x,70,x,290,'stroke="#d4e1d7" stroke-width="1"')
for y in range(70,291,44):b+=line(110,y,660,y,'stroke="#d4e1d7" stroke-width="1"')
b+=line(110,290,675,290)+line(110,290,110,52)+text(49,75,'電圧',16)+text(602,323,'時間 →',16)+path('M111 244h75v-131h150v131h150v-131h150v131h24')+line(110,177,660,177,'stroke="#bb743c" stroke-dasharray="6 5"')+text(383,163,'トリガレベル',14,ACC)+text(19,118,'3.3 V',14)+text(40,249,'0 V',14)+path('M186 270h300')+text(329,272,'T',17)+text(135,324,'例：0〜3.3 Vの矩形波',15,GRAY)
save('scope','矩形波とトリガレベルの概念図',b)
b=text(25,30,'信号を入れて、入力と出力を比べる',19)
b+=f'<rect x="25" y="101" width="110" height="76" rx="5"/>'+text(80,133,'FG',22,anchor='middle')+text(80,157,'Hi-Z設定',13,anchor='middle')+line(135,127,180,127)+rh(180,350,127,'1 kΩ')+line(350,127,400,127)+cv(400,127,262,'100 nF')+line(80,177,80,277)+line(80,277,645,277)+line(400,262,400,277)+gnd(400,277)+dot(180,127)+dot(400,127)
b+=f'<rect x="510" y="60" width="180" height="130" rx="6"/>'+text(600,91,'OSCILLOSCOPE',15,anchor='middle')+text(544,127,'CH1',14,anchor='middle')+text(650,160,'CH2',14,anchor='middle')+path('M180 127V44H544V105')+path('M400 127H465V158H515')+line(575,190,575,277)+line(645,190,645,277)+dot(575,277)+dot(645,277)+text(25,322,'CH1＝R手前のVin　CH2＝C上端のVout　すべて同じGNDへ',14,GRAY)
save('experiment-chain','FGとRCと2チャンネルオシロの接続',b)
b=text(25,30,'ゆっくり見るRCの充放電',19)+text(27,98,'＋3 V',16)+line(90,95,150,95)+dot(150,95)+dot(150,175)+line(90,175,150,175)+gnd(90,175)+dot(210,133)+line(210,133,155,98)+rh(210,455,133,'100 kΩ')+dot(455,133)+cv(455,133,265,'100 µF')+text(427,189,'＋',20)+gnd(455,265)+line(455,133,610,133)+line(610,133,610,172)+f'<circle cx="610" cy="203" r="31"/>'+text(610,211,'V',22,anchor='middle')+line(610,234,610,275)+line(455,275,610,275)+text(85,239,'SPDTで切替',15)+text(47,321,'3 Vで充電、GNDで放電。どちらも100 kΩを通す。τ = 10 s',15,GRAY)
save('rc-step','SPDTと抵抗を使ったコンデンサ充放電回路',b)
b=text(25,30,'12 V → 3.3 Vの電源構成',19)
for x,w,label,sub in [(25,115,'DC 12 V','絶縁済み入力'),(185,100,'入力保護','逆接・過電流'),(335,155,'降圧DC-DC','メーカー推奨C'),(550,140,'マイコン','電源直近にC')]:
 b+=f'<rect x="{x}" y="110" width="{w}" height="80" rx="5"/>'+text(x+w/2,142,label,16,anchor='middle')+text(x+w/2,170,sub,12,GRAY,anchor='middle')+line(x+w/2,190,x+w/2,267)
b+=line(140,140,185,140,'marker-end="url(#arrow)"')+line(285,140,335,140,'marker-end="url(#arrow)"')+line(490,140,550,140,'marker-end="url(#arrow)"')+text(500,115,'3.3 V',15)+line(83,267,620,267)+gnd(380,267)+text(26,328,'方式を示すブロック図。入力・出力C、保護定数は採用モジュールの仕様に従う。',14,GRAY)
save('power','絶縁された12V直流から3.3Vを作るブロック図',b)
b=text(25,30,'信号の流れと、電源・GND',19)
labels=[('センサー','0〜1 V'),('増幅器','ゲイン3'),('ADC','電圧→数値'),('マイコン','判定'),('MOSFET','駆動'),('負荷','5 V / 50 mA')]
for i,(lab,sub) in enumerate(labels):
 x=20+i*116
 b+=f'<rect x="{x}" y="123" width="100" height="82" rx="5"/>'+text(x+50,155,lab,15,anchor='middle')+text(x+50,183,sub,12,GRAY,anchor='middle')
 if i<5:b+=line(x+100,164,x+114,164,'marker-end="url(#arrow)"')
 b+=line(x+50,205,x+50,270)
b+=line(70,270,650,270)+gnd(360,270)+text(30,83,'アナログ信号の基準と負荷電流の帰路を意識する',16,GRAY)+text(30,326,'詳細回路は設計3・5・7を参照。接続点ごとに、単体 → 全体の順で検証。',14,GRAY)
save('system','センサー増幅ADCマイコンMOSFET負荷の機能接続図',b)
b=text(25,30,'回路図の基本記号',19)+rh(40,220,95,'抵抗器 R')+ch(275,455,95,'コンデンサ C')+line(590,65,590,100)+gnd(590,100)+text(590,160,'GND',17,anchor='middle')
b+=rh(40,220,245,'可変抵抗')+path('M172 180L132 236','marker-end="url(#arrow)"')+diode(363,245)+text(365,205,'ダイオード D',17,anchor='middle')+text(329,285,'A',16)+text(387,285,'K',16)+path('M560 215v70M560 229l40-24M560 271l40 28','marker-end="url(#arrow)"')+line(520,250,560,250)+text(612,254,'NPN',17)+text(530,327,'Eの矢印は外向き',13,GRAY)
save('symbols','抵抗コンデンサGND可変抵抗ダイオードNPNの記号',b)
b=text(25,30,'ダイオードの記号と光の向き',19)+diode(160,127)+text(160,79,'整流ダイオード',17,anchor='middle')+text(120,171,'A',16)+text(185,171,'K',16)+diode(530,127,True)+text(530,79,'LED（発光）',17,anchor='middle')+text(480,171,'A',16)+text(550,171,'K',16)
b+=diode(160,266)+path('M183 234l-18 18m0-8v8h8M201 244l-18 18m0-8v8h8')+text(160,217,'フォトダイオード',17,anchor='middle')+text(128,312,'光は内向き',14,GRAY)
b+=path('M485 266h25m0-16 27 16-27 16zM537 250v32l9-6M537 250l-9 6M537 266h28')+text(530,217,'ツェナーダイオード',17,anchor='middle')+text(487,312,'A',16)+text(550,312,'K',16)
save('diode-symbols','ダイオードLEDフォトダイオードツェナーの記号',b)
print('Created',len(list(out.glob('*.svg'))),'original SVG diagrams')
b=text(25,30,'NPN増幅器のDCバイアス',19)+line(170,65,535,65)+text(310,53,'＋5 V',17)+rv(235,65,175,'22 kΩ')+rv(235,175,294,'10 kΩ')+gnd(235,294)+dot(235,175)+line(235,175,402,175)+line(402,145,402,210)+line(402,157,440,131)+rv(440,65,131,'RC 2.2 kΩ')+dot(440,131)+line(440,131,645,131)+text(552,111,'VC ≈ 3.24 V',15)+path('M402 195L440 222','marker-end="url(#arrow)"')+rv(440,222,294,'RE 1 kΩ')+gnd(440,294)+text(43,217,'VB ≈ 1.51 V',14)+text(29,331,'5 V、VBE = 0.7 V、β = 100という計算上の仮定。交流入力は別途結合Cで接続。',13,GRAY)
save('bjt-bias','ベース分圧とエミッタ抵抗で安定化したBJTバイアス回路',b)
# Matching schematic for the PWM design uses a 100-ohm load.
s=(out/'mosfet.svg').read_text().replace('負荷 1 kΩ','負荷 100 Ω').replace('図は抵抗負荷の例。','抵抗は0.5 W以上の適切な定格。')
(out/'mosfet-pwm.svg').write_text(s)
b=text(25,30,'半波整流と平滑（共通GND）',19)+text(40,85,'低電圧AC入力',16)+line(75,120,185,120)+diode(220,120)+line(255,120,590,120)+dot(390,120)+cv(390,120,265,'C')+text(356,180,'＋',20)+rv(590,120,265,'RL')+line(75,275,590,275)+line(390,265,390,275)+line(590,265,590,275)+gnd(390,275)+text(481,98,'Vout',16)+text(40,304,'入力GND',15)+text(37,336,'Dで正側だけ通す → Cが谷を補う。FGの出力電流・突入・C極性に注意。',13,GRAY)
save('rectifier','ダイオード半波整流とコンデンサ平滑と抵抗負荷',b)
b=text(25,30,'比較器：オープンドレイン出力の例',19)+path('M265 95L265 243L420 168z')+text(283,140,'＋',22)+text(283,210,'−',22)+line(50,132,265,132)+text(40,108,'センサー入力',16)+line(50,205,265,205)+text(42,239,'基準電圧 Vref',16)+line(420,168,655,168)+dot(525,168)+rv(525,59,168,'Rpull-up')+text(488,47,'＋3.3 V',16)+text(576,148,'出力',16)+text(445,232,'入力 > Vref：H',15)+text(445,265,'入力 < Vref：L',15)+text(30,324,'電源端子とデカップリングは省略。入力範囲・出力耐圧・ヒステリシスを確認。',13,GRAY)
save('comparator','比較器の入力とプルアップを持つ出力',b)
b=text(25,30,'シュミットインバータのRC発振',19)+path('M275 90L275 240L430 165z')+f'<circle cx="440" cy="165" r="10"/>'+path('M300 133h13v36h13v-22m-13 22v25h-13v-27')+line(140,165,275,165)+dot(185,165)+line(450,165,620,165)+dot(545,165)+line(545,165,545,65)+rh(185,545,65,'R')+line(185,65,185,165)+cv(185,165,280,'C')+gnd(185,280)+text(566,144,'出力',16)+text(270,289,'上下のしきい値の間を充放電',16)+text(35,332,'周期はR・CだけでなくICのしきい値にも依存。電源・デカップリングは省略。',13,GRAY)
save('oscillator','シュミットインバータ出力からRCへ帰還する発振回路',b)
print('Final diagram count:',len(list(out.glob('*.svg'))))
