set -ex

RAW_EN=corpus/raw_en.txt
RAW_RU=corpus/raw_ru.txt

paste $RAW_RU $RAW_EN > raw.ruen
python src/filter.py raw.ruen train test valid

python src/learn.py --input train.ruen --prefix bpe --vocab-size 4000 --character-coverage 0.9995 --threads 1


encode () {
    python src/encode.py --model bpe.model
}

encode < train.en > train.bpe.en
encode < train.ru > train.bpe.ru
encode < test.en > test.bpe.en
encode < test.ru > test.bpe.ru

fairseq-preprocess -s en -t ru \
    --trainpref train.bpe \
    --validpref valid \
    --destdir data-bin \
    --joined-dictionary