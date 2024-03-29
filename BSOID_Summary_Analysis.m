handX_velS = smoothdata(handX_vel(:,1),'gaussian',10);

figure(1)
clf
plot(handX_vel(:,2),handX_vel(:,1))
hold on
plot(handX_vel(:,2),handX_velS(:,1))

noseX_velS = smoothdata(noseX_vel(:,1),'gaussian',15);

figure(2)
clf
plot(noseX_vel(:,2),noseX_vel(:,1))
hold on
plot(noseX_vel(:,2),noseX_velS(:,1))

bsoidGroupIDs = unique(bsoid_labels(:,1));

bsoidGroupHandX = nan(100000,length(bsoidGroupIDs));
bsoidGroupHandX_vel = nan(100000,length(bsoidGroupIDs));
bsoidGroupNoseX = nan(100000,length(bsoidGroupIDs));
bsoidGroupNoseX_vel = nan(100000,length(bsoidGroupIDs));

for bgInd = 1:length(bsoidGroupIDs)

    groupInds = find(bsoid_labels == bsoidGroupIDs(bgInd));

    handXvals = rmoutliers(handX(groupInds,1));
    handXVeloVals = rmoutliers(handX_velS(groupInds,1));
    noseXvals = rmoutliers(noseX(groupInds,1));
    noseXVeloVals = rmoutliers(noseX_velS(groupInds,1));

    bsoidGroupHandX(1:length(handXvals),bgInd) = (handXvals);
    bsoidGroupHandX_vel(1:length(handXVeloVals),bgInd) = (handXVeloVals);
    bsoidGroupNoseX(1:length(noseXvals),bgInd) =  (noseXvals);
    bsoidGroupNoseX_vel(1:length(noseXVeloVals),bgInd) = (noseXVeloVals);

end

HandPosStats = table(bsoidGroupIDs, mean(bsoidGroupHandX,'omitnan')', std(bsoidGroupHandX,'omitnan')',sum(~isnan(bsoidGroupHandX))','VariableNames',{'GroupID','mean','std','n'});
NosePosStats =  table(bsoidGroupIDs, mean(bsoidGroupNoseX,'omitnan')', std(bsoidGroupNoseX,'omitnan')', sum(~isnan(bsoidGroupNoseX))','VariableNames',{'GroupID','mean','std','n'});

HandVelStats =  table(bsoidGroupIDs, mean(bsoidGroupHandX_vel,'omitnan')', std(bsoidGroupHandX_vel,'omitnan')', sum(~isnan(bsoidGroupHandX_vel))','VariableNames',{'GroupID','mean','std','n'});
NoseVelStats =  table(bsoidGroupIDs, mean(bsoidGroupNoseX_vel,'omitnan')', std(bsoidGroupNoseX_vel,'omitnan')', sum(~isnan(bsoidGroupNoseX_vel))','VariableNames',{'GroupID','mean','std','n'});

