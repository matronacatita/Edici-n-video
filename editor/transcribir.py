import sys, json, soundfile as sf, sherpa_onnx, glob
m=sys.argv[1]
r=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=glob.glob(m+'/encoder*.onnx')[0],decoder=glob.glob(m+'/decoder*.onnx')[0],joiner=glob.glob(m+'/joiner*.onnx')[0],tokens=m+'/tokens.txt',model_type='nemo_transducer',num_threads=4)
a,sr=sf.read(sys.argv[2],dtype='float32')
s=r.create_stream(); s.accept_waveform(sr,a); r.decode_stream(s)
res=s.result
words=[];cur=None
for tok,t in zip(res.tokens,res.timestamps):
    if tok.startswith(' ') or cur is None:
        if cur: words.append(cur)
        cur=[tok.strip(),t,t]
    else:
        cur[0]+=tok; cur[2]=t
if cur: words.append(cur)
json.dump(words,open(sys.argv[3],'w'),ensure_ascii=False)
print(res.text)
for w in words: print(f"{w[1]:.2f} {w[0]}")
