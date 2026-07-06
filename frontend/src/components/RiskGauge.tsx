import React, { useEffect, useState } from 'react';

interface RiskGaugeProps {
  score: number; // e.g. 822 (out of 1000)
  percentileText: string; // e.g. '94th Percentile Low Risk'
}

export const RiskGauge: React.FC<RiskGaugeProps> = ({ score, percentileText }) => {
  const [offset, setOffset] = useState(440);
  
  useEffect(() => {
    // Total circumference is 2 * Math.PI * 70 = 439.82 (approx 440)
    // Scale score to a percentage (300 is min, 850 is max in FICO space)
    // Or just treat as score/1000
    const scoreFraction = score / 1000;
    const progressOffset = 440 * (1 - scoreFraction);
    
    const timer = setTimeout(() => {
      setOffset(progressOffset);
    }, 100);
    
    return () => clearTimeout(timer);
  }, [score]);

  return (
    <div className="bg-white p-8 rounded-[32px] flex flex-col items-center justify-center relative overflow-hidden shadow-soft">
      <div className="relative w-40 h-40">
        <svg className="w-full h-full transform -rotate-90">
          {/* Track circle */}
          <circle
            className="text-surface-container-low"
            cx="80"
            cy="80"
            fill="transparent"
            r="70"
            stroke="currentColor"
            strokeWidth="12"
          />
          {/* Progress circle */}
          <circle
            className="text-primary transition-all duration-1000 ease-out"
            cx="80"
            cy="80"
            fill="transparent"
            r="70"
            stroke="currentColor"
            strokeWidth="12"
            strokeDasharray="440"
            strokeDashoffset={offset}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-headline text-[40px] font-bold text-primary">{score}</span>
          <span className="font-label text-[10px] text-outline-variant -mt-1 uppercase tracking-wider">Risk Score</span>
        </div>
      </div>
      <p className="mt-4 font-body text-sm text-on-surface-variant text-center px-2">{percentileText}</p>
    </div>
  );
};
