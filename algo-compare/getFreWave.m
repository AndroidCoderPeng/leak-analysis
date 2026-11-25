%  将两个探头接收到的数据进行fft，将20到3000Hz的频谱图赋值给fx 供上位机调用
  

function [fx, freA, freB] = getFreWave(vecA, vecB, fs)

leng = length(vecA);
interval = fs/leng;
f = 0 : interval : fs/2-interval;
freA = abs(fft(vecA))*2/leng;
freB = abs(fft(vecB))*2/leng;

startIndex = 1;
for i=1:length(f)
    if f(i) >= 20
        startIndex = i;
        break;
    end
end

endIndex = length(f);
for j = length(f) : -1 : 1
    if f(j) <= 3000
        endIndex = j;
        break;
    end
end

fx = f(startIndex : endIndex);