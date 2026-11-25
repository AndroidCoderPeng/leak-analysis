function [corrCoeffVec, disVec] = calcuCorrCoeffVec(VecA, VecB, dis, velo, samInter)  

maxTimeDiff = dis/velo*1e6;%单位us 最大传输时间
pointNum = 1 + 2* floor(maxTimeDiff/samInter);
corrCoeffVec = zeros(1, pointNum);
disVec = zeros(1, pointNum);

for i=0:(floor(maxTimeDiff/samInter))%ADI加速度传感器采样频率20kHz，采样间隔50微秒
    corrCoeffVec((pointNum + 1)/2 - i) = calcuCorrCoeff(VecA, VecB, i);
    corrCoeffVec((pointNum + 1)/2 + i) = calcuCorrCoeff(VecB, VecA, i);
    disVec((pointNum + 1)/2 - i) = dis/2 - velo * samInter/2 * i * 1e-6;
    disVec((pointNum + 1)/2 + i) = dis/2 + velo * samInter/2 * i * 1e-6;
end

%L =(D-v*tao)/2


%VecA  传感器A数据  
% VecB 传感器B数据
%dis 传感器A和B之间的距离
%
% velo 声速
% samInter 采样时间间隔
% 
% 
% 

