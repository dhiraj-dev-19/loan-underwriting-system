import React from 'react';

export type PipelineStepIndex = 0 | 1 | 2 | 3 | 4 | 5; // 0 = idle, 5 = all done

interface PipelineTrackerProps {
  activeStep?: PipelineStepIndex;
}

const PIPELINE_AGENTS = [
  { num: '1', label: 'Ingestion' },
  { num: '2', label: 'Scoring' },
  { num: '3', label: 'Cohort' },
  { num: '4', label: 'Explainer' },
  { num: '5', label: 'Recommender' }
];

export const PipelineTracker: React.FC<PipelineTrackerProps> = ({ activeStep }) => {
  return (
    <div className="flex items-center justify-center gap-0 w-full p-4 bg-surface-container-low/50 border border-outline-variant/20 rounded-2xl shadow-sm mb-6">
      {PIPELINE_AGENTS.map((agent, i) => {
        const isDone = activeStep !== undefined && i < activeStep;
        const isActive = activeStep !== undefined && i === activeStep;
        
        let circleClass = "w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs border-2 transition-all duration-300 ";
        let labelClass = "text-[10px] font-label font-medium text-center uppercase tracking-wider mt-1 transition-colors duration-300 ";
        let lineClass = "h-[2px] flex-1 mx-2 mb-4 transition-colors duration-500 ";

        if (isDone) {
          circleClass += "bg-[#ceddc2] border-primary text-primary";
          labelClass += "text-primary font-bold";
          lineClass += "bg-primary";
        } else if (isActive) {
          circleClass += "bg-primary border-primary text-white scale-110 shadow-md ring-4 ring-primary/20";
          labelClass += "text-primary font-bold";
          lineClass += "bg-outline-variant/30";
        } else {
          circleClass += "bg-white border-outline-variant text-outline-variant";
          labelClass += "text-outline-variant";
          lineClass += "bg-outline-variant/30";
        }

        return (
          <React.Fragment key={agent.num}>
            <div className="flex flex-col items-center min-w-[70px]">
              <div className={circleClass}>
                {isDone ? (
                  <span className="material-symbols-outlined text-[16px] font-bold">check</span>
                ) : (
                  agent.num
                )}
              </div>
              <span className={labelClass}>{agent.label}</span>
            </div>
            {i < PIPELINE_AGENTS.length - 1 && <div className={lineClass} />}
          </React.Fragment>
        );
      })}
    </div>
  );
};
