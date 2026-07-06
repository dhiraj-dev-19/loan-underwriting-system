import React from 'react';

export const Settings: React.FC = () => {
  return (
    <div className="p-8 max-w-[1400px] mx-auto space-y-8">
      <div>
        <h2 className="font-headline text-[36px] font-bold text-primary">System Settings</h2>
        <p className="text-on-surface-variant font-body text-sm font-semibold">Configure ML model thresholds and automated underwriting parameters.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Model Thresholds Card */}
        <div className="bg-white p-8 rounded-xxl shadow-soft border border-outline-variant/10">
          <h3 className="font-headline text-lg font-bold text-on-surface mb-6 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-[24px]">tune</span>
            Auto-Underwrite Parameters
          </h3>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-body font-bold text-on-surface-variant">Auto-Approve Threshold</span>
                <span className="font-headline text-sm font-bold text-primary">FICO ≥ 740 &amp; DTI ≤ 30%</span>
              </div>
              <div className="h-2 bg-surface-container rounded-full overflow-hidden">
                <div className="bg-primary h-full rounded-full" style={{ width: '80%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-body font-bold text-on-surface-variant">Auto-Decline Threshold</span>
                <span className="font-headline text-sm font-bold text-secondary">FICO &lt; 580 | DTI &gt; 50%</span>
              </div>
              <div className="h-2 bg-surface-container rounded-full overflow-hidden">
                <div className="bg-secondary h-full rounded-full" style={{ width: '35%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-body font-bold text-on-surface-variant">Default Volatility Limit</span>
                <span className="font-headline text-sm font-bold text-on-surface">5.0% maximum cohort risk</span>
              </div>
              <div className="h-2 bg-surface-container rounded-full overflow-hidden">
                <div className="bg-outline-variant h-full rounded-full" style={{ width: '50%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Integration Status Card */}
        <div className="bg-white p-8 rounded-xxl shadow-soft border border-outline-variant/10">
          <h3 className="font-headline text-lg font-bold text-on-surface mb-6 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-[24px]">power</span>
            Connected Integrations
          </h3>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-surface-container-low rounded-xl">
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-primary">database</span>
                <div>
                  <h4 className="font-headline text-xs font-bold text-on-surface">Google BigQuery</h4>
                  <p className="text-[10px] text-outline font-semibold">Active connection: loan_applicants</p>
                </div>
              </div>
              <span className="px-2.5 py-1 bg-primary-fixed text-primary text-[10px] font-label font-bold rounded-full">ACTIVE</span>
            </div>

            <div className="flex items-center justify-between p-4 bg-surface-container-low rounded-xl">
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-primary">psychology</span>
                <div>
                  <h4 className="font-headline text-xs font-bold text-on-surface">Gemini-1.5-Pro API</h4>
                  <p className="text-[10px] text-outline font-semibold">Model synthesis pipeline active</p>
                </div>
              </div>
              <span className="px-2.5 py-1 bg-primary-fixed text-primary text-[10px] font-label font-bold rounded-full">CONNECTED</span>
            </div>

            <div className="flex items-center justify-between p-4 bg-surface-container-low rounded-xl">
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-primary">memory</span>
                <div>
                  <h4 className="font-headline text-xs font-bold text-on-surface">RAPIDS ML Server</h4>
                  <p className="text-[10px] text-outline font-semibold">GPU execution pool: running</p>
                </div>
              </div>
              <span className="px-2.5 py-1 bg-primary-fixed text-primary text-[10px] font-label font-bold rounded-full">GPU LIVE</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
