# Pedestrian Counter(歩行者カウント) Demo

<div align="center">
    <p>
        <img src="data/gif/output_demo.gif" width="800"/> 
    </p>
</div>

</div>

## Introduction

社内でOpenCVを使用したアルゴリズムの具体例を提示するために作成した
歩行者が上流・下流からそれぞれ何人歩いてきたかをカウントする歩行者量調査アルゴリズムです。

## Requirement

* python 3.8
* numpy 1.21.0
* opencv-python 4.5.3.56
* pandas 1.2.4

## Installation

Dockerを使用しない場合

```bash
cd pedestrian-counter-demo
pip install -r requirements.txt
```

## Usage

```bash
git clone https://github.com/ac2393921/pedestrian-counter-demo.git
cd pedestrian-counter-demo
docker-compose up -d --build
docker-compose exec python3 bash

# コンテナ内で
cd src
python main.py
```

## Note

trackingデータを作成したモデルをipynb形式で`/model`に上げています。
[Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb?hl=ja)で試しみてください。

## License
pedestrian-counter-demo is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).