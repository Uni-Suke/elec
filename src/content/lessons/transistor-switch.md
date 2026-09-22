---
title: "トランジスタスイッチ：ベース抵抗の役割"
category: "circuits"
order: 4
description: "NPNでLEDをON/OFFし、ベース電流と飽和電圧を確認します。"
minutes: 10
level: "基礎"
tags: ["トランジスタスイッチ", "BJT", "NPN", "ベース抵抗", "飽和"]
objectives: ["NPNでLEDをON/OFFし、ベース電流と飽和電圧を確認します。"]
related: ["transistors", "lab-06", "design-02"]
reviewed: "2026-09-19"
quiz: {"question": "GPIOはHなのにCが2 Vあり、LEDが暗い。候補は？", "answer": "ベース電流不足、端子配列違い、負荷過大、GPIOの電圧低下などが考えられます。GPIO、RB両端、VBE、VCEを測って順に絞ります。"}
diagram: "bjt"
diagramCaption: "NPNの低側スイッチ。ベース抵抗とLED直列抵抗は、それぞれ別の電流を制限する。"
---

## まず直感で：GPIOは指示、電源は仕事をする
GPIOから負荷電流を全部供給せず、NPNをGND側のスイッチにします。LEDの電流は5 V電源から流れ、GPIOは小さなベース電流だけを供給します。

## 回路の接続
5 V→LED用抵抗→LED→NPNのC、E→GND。GPIO→ベース抵抗RB→B。マイコンGNDと負荷電源GNDを共通にします。B-E間にプルダウンを入れると、GPIOが入力になる起動時にOFFしやすくなります。

## 2本の抵抗の違い
LED抵抗は負荷の電流を決め、RBはB-E接合へ流す電流を制限します。LED用抵抗だけではGPIOを守れません。RBをなくすとB-E接合がダイオードとして流れ、GPIOやBJTを損傷する可能性があります。

## 飽和を見込んで計算する
IC = 10 mA、強制電流増幅率IC/IB = 10を設計上の出発点にするとIB = 1 mA。GPIO高レベル3.3 V、VBE ≈ 0.8 VならRB ≈ 2.5 kΩ。実際にはGPIOの最小VOHとVBE(sat)最大、プルダウン電流も考慮します。常に倍率10でよいのではなく、採用品のVCE(sat)保証条件を使います。

## 値を変える・故障するとどうなるか
RBが大きすぎると十分飽和せずVCEが上がり、負荷電流が減る・BJTが発熱することがあります。RBが小さすぎればGPIOが過負荷。C-E短絡では常時ON、RB断線なら通常OFFです。EとCを取り違えると似た動きをしても性能が大きく悪化します。

## 測定点
GND基準でGPIO、B、Cを測ります。ON時、BはEより約0.7〜0.9 V高く、Cは低い電圧になるのが目安。数値は品種・電流で変わります。RB両端の電圧からベース電流、LED抵抗の電圧から負荷電流を求めます。
