time = handX(:,2);

[~,reachIndsLaser] = intersect(round(time,2),round(beamBreakTimesLaser,2));
[~,reachIndsNoLaser] = intersect(round(time,2),round(beamBreakTimesNoLaser,2));
threshold = -2;

%%
figure(1)
clf
subplot(121)
histogram(handX(reachIndsLaser,1),25)
xlabel({'Hand x position','at beam beak with laser (mm)'})
ylabel('number of observations')
hold on
line([threshold;threshold],get(gca,'YLim'),'color','g','linestyle','--','linewidth',2)
title(['Threshold == ' num2str(threshold)])
axis square

subplot(122)
histogram(handX(reachIndsNoLaser,1),25)
xlabel({'Hand x position','at beam beak with NO laser (mm)'})
ylabel('number of observations')
hold on
line([threshold;threshold],get(gca,'YLim'),'color','g','linestyle','--','linewidth',2)
title(['Threshold == ' num2str(threshold)])
axis square

beamBreakTimesNoLaserHand = beamBreakTimesNoLaser(handX(reachIndsNoLaser,1) > threshold);
beamBreakTimesNoLaserNose = beamBreakTimesNoLaser(handX(reachIndsNoLaser,1) <= threshold);





beamBreakTimesLaserHand = beamBreakTimesLaser(handX(reachIndsLaser,1) > threshold);
beamBreakTimesLaserNose = beamBreakTimesLaser(handX(reachIndsLaser,1) <= threshold);


