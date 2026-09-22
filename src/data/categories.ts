export const categories = [
 {id:'basics', name:'電子回路の基礎', en:'FUNDAMENTALS', icon:'wave', color:'green', description:'電圧・電流から回路図まで。すべての土台をつくる。', goal:'電流の道筋を追い、回路の電圧を計算できる'},
 {id:'components', name:'電子部品を知る', en:'COMPONENTS', icon:'resistor', color:'blue', description:'働き、選び方、壊れ方。部品の「なぜ」を理解する。', goal:'データシートを読み、部品の役割と制約を説明できる'},
 {id:'circuits', name:'基本回路を読む', en:'BASIC CIRCUITS', icon:'circuit', color:'purple', description:'部品がつながると、何が起こる？定番回路を読み解く。', goal:'部品をなくす・値を変えるとどうなるか予測できる'},
 {id:'measurement', name:'測定器を使う', en:'MEASUREMENT', icon:'scope', color:'orange', description:'テスターからオシロまで。見えない電気を確かめる。', goal:'目的に合う測定器を選び、安全に接続して読める'},
 {id:'experiments', name:'実験で確かめる', en:'HANDS-ON LAB', icon:'flask', color:'teal', description:'低電圧の小さな実験で、知識を手応えに変える。', goal:'予測と測定の違いを記録し、原因を考えられる'},
 {id:'troubleshooting', name:'故障を切り分ける', en:'TROUBLESHOOTING', icon:'search', color:'red', description:'動かない理由を、順序立てて見つける。', goal:'電源から信号へ、根拠を持って故障箇所を絞れる'},
 {id:'design', name:'回路を設計する', en:'CIRCUIT DESIGN', icon:'pencil', color:'green', description:'仕様から部品選定、実測まで。自分の回路をつくる。', goal:'要求仕様から簡単な回路とBOMを作り、評価できる'},
] as const;
export const categoryById = (id: string) => categories.find(c=>c.id===id)!;
