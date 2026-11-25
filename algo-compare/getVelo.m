% 4.3	ÉùËÙµ÷ÓÃ´úÂë
function velo = getVelo(material, diamLow, diamHigh)    
    %1.ÇòÌú
    matrix1 =    [0  99	1320
                100 199	1250
                200 299	1190
                300 399	1160
                400 599	1130
                600 799	1080
                800 899	1060
               1000	 -1 1030];
               
    %2.ÖýÌú
    matrix2 =    [0  99	1280
                100 199	1220
                200 299	1160
                300 399	1130
                400 499	1100
                500 699	1080
                700  -1	1030]  ;

    %3.¸Ö
    matrix3 =    [0  19	1400
                 20  99	1300
                100 199	1200
                200 299	1120
                300 499	1040
                500 699	1020
                700 899	 970
                900  -1	 900];
            
    %4.Í­
    matrix4 =   [0 14	1260
                15 24	1230
                25 59	1180
                60 -1	1150]; 
    
    %5.Ç¦      
    matrix5 =   [0 19	1200
                20 -1	1150]; 
            
    %6.Ë®Äà
    matrix6 =    [0 99	1100
                100 199	1000
                200 349	960
                350 499	960
                500 699	910
                700 899	900
                900  -1	880];
            
    %7.PVC
    matrix7 =   [0 17	650
                18 22	630
                23 27	600
                28 49	540
                50 74	520
                75 99	480
               100 199	460
               200  -1	440];
           
    %8.HDPE
    matrix8 =   [0  17	360
                18  22	330
                23  74	300
                75 199	300
               200  -1  300];
           
    %9.MDPE
    matrix9 =   [0  17	300
                18  22	270
                23  74	240
                75 199	240
               200  -1	250];
           
    %10.²£Á§¸Ö
    matrix10 =    [0   49	1300
                  50   99	1280
                 100  199	1210
                 200  399	1180
                 400  799	1160
                 800 1199	1150
                1200 1999	1150
                2000   -1	1140];
            
    %11.»ìÄýÍÁ
    matrix11 =   [0  499	1160
                500  699	1100
                700  899	1030
                900 1199	1020
               1200 1799	1010
               1800   -1	1000];
           
    %12.Õ³ÍÁ
    matrix12 =   [0  99	1100
                100 199	1100
                200 349	1100
                350 499	1100
                500 699	1100
                700 899	1100
                900  -1	1100];
            
    %13.LDPE
    matrix13 =   [0 17	310
                18 22	290
                23 74	230
                75 -1	230];
         
    switch material
        case 1
            veloMatr = matrix1;
        case 2
            veloMatr = matrix2;
        case 3
            veloMatr = matrix3;
        case 4
            veloMatr = matrix4;
        case 5
            veloMatr = matrix5;
        case 6
            veloMatr = matrix6;
        case 7
            veloMatr = matrix7;
        case 8
            veloMatr = matrix8;
        case 9
            veloMatr = matrix9;
        case 10
            veloMatr = matrix10;
        case 11
            veloMatr = matrix11;
        case 12
            veloMatr = matrix12;
        case 13
            veloMatr = matrix13;
        otherwise
            veloMatr = zeros(0, 3);
    end
    
    %ÉèÖÃÄ¬ÈÏÖµ
    velo = 1195;
    diamLow = floor(diamLow);
    diamHigh =floor(diamHigh);
    n = length(veloMatr);
    if diamLow ~= diamHigh
        for i=1:n
           line = veloMatr(i,:);
           if line(1) == diamLow && line(2) == diamHigh
               velo = line(3);
               break;
           end
        end
    else 
        for i=1:n
           line = veloMatr(i,:);
           if (line(1) <= diamLow && line(2) >= diamLow) || (line(1) <= diamLow && line(2) == -1)
               velo = line(3);
               break;
           end
        end
    end
end