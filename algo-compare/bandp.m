function [y, success]=bandp(x,f1,f3,fsl,fsh,rp,rs,Fs)
%VecA',freLow,freHigh,freLow*cutCoefLow,freHigh*cutCoefHigh,0.5,rs,fs
%带通滤波
%使用注意事项：通带或阻带的截止频率与采样率的选取范围是不能超过采样率的一半
%即，f1,f3,fs1,fsh,的值小于 Fs/2
%x:需要带通滤波的序列
% f 1：通带左边界 
% f 3：通带右边界
% fs1：衰减截止左边界
% fsh：衰变截止右边界
%rp：边带区衰减DB数设置  passband 
%rs：截止区衰减DB数设置
%FS：序列x的采样频率
% f1=300;f3=500;%通带截止频率上下限
% fsl=200;fsh=600;%阻带截止频率上下限
% rp=0.1;rs=30;%通带边衰减DB值和阻带边衰减DB值
% Fs=2000;%采样率
% Stopband corner frequency Ws, is a scalar or a two-element vector with values between 0 and 1
% , with 1 corresponding to the normalized Nyquist frequency.
%
%% 设计巴特沃斯
% [n,wn] = buttord(wp/pi,ws/pi,rp,rs);
% [b,a] = butter(n,wn);
% y = filter(b,a,x) ;
% figure;
% plot(y);


%% 切比雪夫2型
% [n,wn]=cheb2ord(wp,ws,rp,rs,'s');       %求切比雪夫II型滤波器阶数
% fprintf('切比雪夫II型滤波 器 N= %4d\n',n);%显示滤波器阶数
% [b,a]=cheby2(n,rs,wn,'s');          %求切比雪夫II型滤波器系数，即求传输函数的分子和分母的系数向量
% [Hc2,wc2]=freqs(b,a,Fs);             %求切比雪夫II型滤波器频率响应
% plot(wc2/pi,20*log10(abs(Hc2)),'r');    %作图
%% FFT
% y=x;
% fs=Fs;
% N=Fs;
% Y=fft(y);
% magY=abs(Y(1:1:N/2))*2/N; 
% f=(0:N/2-1)'*fs/N;  %分辨率fs/N=1/N*ts   
% % figure(2)
% %plot(f,magY);
% % h=stem(f,magY,'fill','--');
% h1=plot(f,magY);
% y = filter(b,a,x) ;
% %% 
% N=Fs;
% Y=fft(y);
% magY=abs(Y(1:1:N/2))*2/N; 
% f=(0:N/2-1)'*fs/N;  %分辨率fs/N=1/N*ts   
% % figure(2)
% %plot(f,magY);
% % h=stem(f,magY,'fill','--');
% figure;
% h2=plot(f,magY);
%% 



%% 设计切比雪夫滤波器；
fs=Fs;
rp=1;rs=40;
wp = [f1 f3] / (fs/2);  %通带截止频率,50~100、200~400中间各取一个值,并对其归一化
ws = [fsl fsh] / (fs/2);  %阻带截止频率,50~100、200~400中间各取一个值,并对其归一化
%获取阶数和截止频率
[ N3 wn ] = cheb2ord( wp , ws , rp , rs);
%获得转移函数系数
[ bz1 az1 ] = cheby2(N3,rs,wn,'bandpass');
% y=filter(bz1,az1,x);
y=filtfilt(bz1,az1,x);%双向滤波实现0相位差异滤波，保证时研法不出现其他的延时
end

% 对于以1000赫兹采样的数据，设计一个低通滤波器，其通带纹波小于3分贝（定义为0至40赫兹），阻带纹波至少60分贝（定义为150赫兹至奈奎斯特频率）。
% Matlab代码如下
% 
% fs=1000;%采样频率
% fn=fs/2;%奈奎斯特频率
% Wp=40/fn;Ws=150/fn;%低通滤波器的通过频带（0-40），阻带（150-fn）
% Rp=3;Rs=60;%通带波纹与阻带波纹的设置--通常依据现实情况判断
% [n,Wn]=cheb1ord(Wp,Ws,Rp,Rs);%获得构建切比雪夫滤波器的最小阶数
% [b,a]=cheby1(n,Rp,Wn);%设计切比雪夫Ⅰ型滤波器
% freqz(b,a);%频域响应



