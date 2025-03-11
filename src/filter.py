import sys
import collections
import random

# フィルタリング条件
MIN_TOKENS = 4
MAX_TOKENS = 16
RATIO_MIN = 0.5
RATIO_MAX = 1.8
MIN_FREQUENCY = 2  # border for the low frequency
TRAIN_RATIO = 0.9  #  Test data ratio 90%
TEST_RATIO = 0.5  # test to valid ration 50%

def tokenize(text):
    """ tokenize with space """
    return text.strip().split()

def filter_and_split_sentences(input_file, train_prefix, test_prefix, valid_prefix):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # make the pairs (ru-en)
    sentence_pairs = [line.split('\t') for line in lines if '\t' in line]
    
    # word counts (for calculate freqency)
    word_counts = collections.Counter()
    for ru, en in sentence_pairs:
        word_counts.update(tokenize(ru))
        word_counts.update(tokenize(en))

    # List for low freq words
    low_freq_words = {word for word, count in word_counts.items() if count < MIN_FREQUENCY}

    filtered_sentences = set()  # delete duplicate
    shuffled_pairs = [] 

    for ru, en in sentence_pairs:
        ru_tokens = tokenize(ru)
        en_tokens = tokenize(en)

        # 1. Check for the number of tokens
        if not (MIN_TOKENS <= len(ru_tokens) <= MAX_TOKENS):
            continue
        if not (MIN_TOKENS <= len(en_tokens) <= MAX_TOKENS):
            continue

        # 2. Check token ration
        ratio = len(ru_tokens) / len(en_tokens)
        if not (RATIO_MIN <= ratio <= RATIO_MAX):
            continue

        # 3. Check low freq words from the list created above
        if any(word in low_freq_words for word in ru_tokens) or any(word in low_freq_words for word in en_tokens):
            continue

        # 4. Check for duplicate based on the list above
        pair_str = f"{ru}\t{en}"
        if pair_str in filtered_sentences:
            continue
        filtered_sentences.add(pair_str)
        shuffled_pairs.append((ru, en))

    # ランダムシャッフル
    random.shuffle(shuffled_pairs)

    # 80% を訓練データ、20% をテストデータに分割
    train_size = int(len(shuffled_pairs) * TRAIN_RATIO)
    train_pairs = shuffled_pairs[:train_size]
    left_pairs = shuffled_pairs[train_size:]
    test_size = int(len(left_pairs) * TEST_RATIO)
    test_pairs = left_pairs[:test_size]
    valid_pairs = left_pairs[test_size:]


    # 訓練データ `train.ruen` を保存
    with open(f"{train_prefix}.ruen", 'w', encoding='utf-8') as f:
        for ru, en in train_pairs:
            f.write(f"{ru}\t{en}\n")

    # 訓練データ `train.ru` / `train.en` を保存
    with open(f"{train_prefix}.ru", 'w', encoding='utf-8') as f_ru, \
         open(f"{train_prefix}.en", 'w', encoding='utf-8') as f_en:
        for ru, en in train_pairs:
            f_ru.write(ru + '\n')
            f_en.write(en + '\n')

    # テストデータ `test.ru`, `test.en` を保存
    with open(f"{test_prefix}.ru", 'w', encoding='utf-8') as f_ru, \
         open(f"{test_prefix}.en", 'w', encoding='utf-8') as f_en:
        for ru, en in test_pairs:
            f_ru.write(ru + '\n')
            f_en.write(en + '\n')

    # 検証データ `valid.ru` / `valid.en` を保存
    with open(f"{valid_prefix}.ru", 'w', encoding='utf-8') as f_ru, \
         open(f"{valid_prefix}.en", 'w', encoding='utf-8') as f_en:
        for ru, en in valid_pairs:
            f_ru.write(ru + '\n')
            f_en.write(en + '\n')

if __name__ == "__main__":
    input_file = sys.argv[1]
    train_prefix = sys.argv[2]
    test_prefix = sys.argv[3]
    valid_prefix = sys.argv[4]
    filter_and_split_sentences(input_file, train_prefix, test_prefix, valid_prefix)


