import vaporetto
import zstandard

#dict_path = 'bccwj-suw+unidic_pos+pron/bccwj-suw+unidic_pos+pron.model.zst'
dict_path = 'bccwj-suw+unidic+tag-lemma/bccwj-suw+unidic+tag-lemma.model.zst'

dctx = zstandard.ZstdDecompressor()
with open(dict_path, 'rb') as fp:
    with dctx.stream_reader(fp) as dict_reader:
        tokenizer = vaporetto.Vaporetto(dict_reader.read(), predict_tags = True)

text = '「吾輩は猫である」。忙しかった。'

toks = tokenizer.tokenize(text)

for tok in toks:
    print(tok.n_tags())
    for tag_id in range(tok.n_tags()):
        print("tag", tok.tag(tag_id))

    print("{}\t{}".format(tok.surface(), tok.tag(0)))


# Print with jagger friendly format
