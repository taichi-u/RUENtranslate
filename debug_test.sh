fairseq-interactive data-bin \
    --buffer-size 1024 \
    --batch-size 128 \
    --path /Users/taichi/document/Tleezインターン/ru-en_translation/checkpoints/checkpoint10.pt \
    --beam 5 \
    --lenpen 0.6 \
    < test.bpe.ru \
    | tee raw_output.txt
