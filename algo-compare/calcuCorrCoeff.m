function [corrCoeff] = calcuCorrCoeff(VecA, VecB, i)

% for jjj=1:length(VecA)
%     disp(['6VecA(', num2str(jjj), '):', num2str(VecA(jjj))]);
%     disp(['6VecB(', num2str(jjj), '):', num2str(VecB(jjj))]);
% end

sizeA = length(VecA);
sizeB = length(VecB);
% disp(['i:', num2str(i)]);
% disp(['sizeA:', num2str(sizeA)]);
% disp(['sizeB:', num2str(sizeB)]);
vec = zeros(max(sizeA, i + sizeB), 2);
% disp(['max(sizeA, i + sizeB):', num2str(max(sizeA, i + sizeB))]);
vec( max(1, i+1) : min(sizeA, i+sizeB), 1) = VecA(max(1, i+1) : min(sizeA, i+sizeB));
vec( max(1, i+1) : min(sizeA, i+sizeB), 2) = VecB(1 : min(sizeA-i, sizeB));
% for jjj=1:max(sizeA, i + sizeB)
%     disp(['vec(', num2str(jjj),',1)', ':', num2str(vec(jjj,1))]);
%     disp(['vec(', num2str(jjj),',2)', ':', num2str(vec(jjj,2))]);
% end
corrCoeffMatr = corrcoef(vec);
% disp(['corrCoeffMatr:',num2str(corrCoeffMatr(1,1)),',',num2str(corrCoeffMatr(1,2)),',',num2str(corrCoeffMatr(2,1)),',',num2str(corrCoeffMatr(2,2))]);
corrCoeff = corrCoeffMatr(1, 2);

