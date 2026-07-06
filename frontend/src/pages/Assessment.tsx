import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import type { ApplicantDetails, UnderwritingResult } from '../types';
import { ApplicantService } from '../services/api';
import { RiskGauge } from '../components/RiskGauge';
import { PipelineTracker } from '../components/PipelineTracker';
import type { PipelineStepIndex } from '../components/PipelineTracker';
import { BarChart, Bar, ResponsiveContainer } from 'recharts';

export const Assessment: React.FC = () => {
  const [activeStep, setActiveStep] = useState<PipelineStepIndex | undefined>(undefined);
  const [result, setResult] = useState<UnderwritingResult | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const { register, handleSubmit, setValue } = useForm<ApplicantDetails>({
    defaultValues: {
      name: 'Eleanor Vance',
      dob: '05/12/1988',
      ssn: '***-**-6789',
      employer: 'NVIDIA Corporation',
      income: 185000,
      tenure: 4.5,
      fico: 782,
      dti: 22,
      outstandingDebt: '$42,000 (Student, Auto)',
      requestedAmount: 650000,
      term: '30 Years Fixed'
    }
  });

  // Mock presets to load into form for demo purposes (matching Point 4 / Sidebar / Streamlit presets)
  const loadPreset = (presetName: string) => {
    if (presetName === 'low') {
      setValue('name', 'Sarah Jenkins');
      setValue('employer', 'Google LLC');
      setValue('income', 150000); // 12500 * 12
      setValue('dti', 15);
      setValue('fico', 810);
      setValue('tenure', 6);
      setValue('outstandingDebt', 'None');
      setValue('requestedAmount', 450000);
    } else if (presetName === 'borderline') {
      setValue('name', 'Marcus Thorne');
      setValue('employer', 'Stripe Inc');
      setValue('income', 54000); // 4500 * 12
      setValue('dti', 48);
      setValue('fico', 630);
      setValue('tenure', 2);
      setValue('outstandingDebt', '$18,000 credit cards');
      setValue('requestedAmount', 250000);
    } else if (presetName === 'high') {
      setValue('name', 'Robert Kensington');
      setValue('employer', 'Contractor');
      setValue('income', 18000); // 1500 * 12
      setValue('dti', 120);
      setValue('fico', 510);
      setValue('tenure', 0.5);
      setValue('outstandingDebt', '$85,000 loans');
      setValue('requestedAmount', 150000);
    }
  };

  const onSubmit = async (data: ApplicantDetails) => {
    setIsEvaluating(true);
    setResult(null);

    // Sequential agent pipeline simulator
    // Step 0: Ingestion
    setActiveStep(0);
    await new Promise(r => setTimeout(r, 400));
    
    // Step 1: Scoring
    setActiveStep(1);
    await new Promise(r => setTimeout(r, 450));
    
    // Step 2: Cohort
    setActiveStep(2);
    await new Promise(r => setTimeout(r, 450));
    
    // Step 3: Explainer
    setActiveStep(3);
    await new Promise(r => setTimeout(r, 450));
    
    // Step 4: Recommender
    setActiveStep(4);
    await new Promise(r => setTimeout(r, 400));

    try {
      const evaluationResult = await ApplicantService.evaluate(data);
      setResult(evaluationResult);
      setActiveStep(5); // all done
    } catch (e) {
      console.error(e);
    } finally {
      setIsEvaluating(false);
    }
  };

  // Mock data for supporting evidence credit velocity bar chart
  const evidenceData = [
    { name: 'Jan', value: 40 },
    { name: 'Feb', value: 45 },
    { name: 'Mar', value: 60 },
    { name: 'Apr', value: 55 },
    { name: 'May', value: 75 },
    { name: 'Jun', value: 80 },
    { name: 'Jul', value: 95 }
  ];

  return (
    <div className="p-8 max-w-[1400px] mx-auto h-[calc(100vh-32px)] flex flex-col gap-6 overflow-hidden">
      {/* Page Header */}
      <header className="flex justify-between items-center flex-shrink-0">
        <div>
          <h2 className="font-headline text-[32px] font-bold text-primary tracking-tight">New Assessment</h2>
          <p className="text-on-surface-variant font-body text-xs font-semibold italic">Application ID: #UN-8921-X</p>
        </div>

        {/* Preset controls */}
        <div className="flex gap-2">
          <button 
            type="button" 
            onClick={() => loadPreset('low')}
            className="px-3.5 py-1.5 bg-[#d1fae5] hover:bg-[#6ee7b7]/30 text-[#065f46] text-[11px] font-label font-bold rounded-full transition-all border border-[#6ee7b7]/45"
          >
            🟢 Low Risk Preset
          </button>
          <button 
            type="button" 
            onClick={() => loadPreset('borderline')}
            className="px-3.5 py-1.5 bg-[#fef3c7] hover:bg-[#fcd34d]/30 text-[#92400e] text-[11px] font-label font-bold rounded-full transition-all border border-[#fcd34d]/45"
          >
            🟡 Borderline Preset
          </button>
          <button 
            type="button" 
            onClick={() => loadPreset('high')}
            className="px-3.5 py-1.5 bg-[#fee2e2] hover:bg-[#fca5a5]/30 text-[#991b1b] text-[11px] font-label font-bold rounded-full transition-all border border-[#fca5a5]/45"
          >
            🔴 High Risk Preset
          </button>
        </div>
      </header>

      {/* Main split dashboard panels */}
      <div className="flex-1 flex gap-6 overflow-hidden min-h-0 pb-16">
        
        {/* Left Side: Applicant Form (40%) */}
        <section className="w-[40%] flex flex-col overflow-y-auto pr-2 custom-scrollbar">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            
            {/* Personal Profile */}
            <div className="p-6 bg-white rounded-xxl shadow-soft border border-outline-variant/10">
              <h3 className="font-headline text-md font-bold text-primary mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-lg">person</span>
                Personal Profile
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Full Name</label>
                  <input
                    {...register('name')}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="text"
                  />
                </div>
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">DOB</label>
                  <input
                    {...register('dob')}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="text"
                  />
                </div>
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">SSN (Masked)</label>
                  <input
                    {...register('ssn')}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="text"
                  />
                </div>
              </div>
            </div>

            {/* Employment & Income */}
            <div className="p-6 bg-white rounded-xxl shadow-soft border border-outline-variant/10">
              <h3 className="font-headline text-md font-bold text-primary mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-lg">work</span>
                Employment &amp; Income
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Employer</label>
                  <input
                    {...register('employer')}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="text"
                  />
                </div>
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Annual Gross Income ($)</label>
                  <input
                    {...register('income', { valueAsNumber: true })}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="number"
                  />
                </div>
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Tenure (Years)</label>
                  <input
                    {...register('tenure', { valueAsNumber: true })}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="number"
                    step="0.1"
                  />
                </div>
              </div>
            </div>

            {/* Debt & Credit History */}
            <div className="p-6 bg-white rounded-xxl shadow-soft border border-outline-variant/10">
              <h3 className="font-headline text-md font-bold text-primary mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-lg">credit_card</span>
                Debt &amp; Credit History
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Credit Score (FICO)</label>
                  <input
                    {...register('fico', { valueAsNumber: true })}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="number"
                  />
                </div>
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">DTI Ratio (%)</label>
                  <input
                    {...register('dti', { valueAsNumber: true })}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="number"
                  />
                </div>
                <div className="col-span-2">
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Outstanding Debt</label>
                  <input
                    {...register('outstandingDebt')}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="text"
                  />
                </div>
              </div>
            </div>

            {/* Loan Details */}
            <div className="p-6 bg-white rounded-xxl shadow-soft border border-outline-variant/10">
              <h3 className="font-headline text-md font-bold text-primary mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-lg">request_quote</span>
                Loan Details
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Requested Amount ($)</label>
                  <input
                    {...register('requestedAmount', { valueAsNumber: true })}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="number"
                  />
                </div>
                <div>
                  <label className="font-label text-[10px] font-bold uppercase text-outline mb-1 block tracking-wider">Term</label>
                  <input
                    {...register('term')}
                    className="w-full bg-surface-container-low border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:bg-white transition-all text-on-surface text-sm outline-none font-body font-semibold"
                    type="text"
                  />
                </div>
              </div>
            </div>
            
            {/* Submit Button Container */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={isEvaluating}
                className="w-full bg-primary hover:bg-primary-container text-white py-4 rounded-full font-headline text-base font-bold flex items-center justify-center gap-3 shadow-xl transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:hover:scale-100"
              >
                <span className="material-symbols-outlined">bolt</span>
                {isEvaluating ? 'Running Decision Engine...' : 'Evaluate Application'}
              </button>
            </div>
          </form>
        </section>

        {/* Right Side: Results Intelligence (60%) */}
        <section className="w-[60%] flex flex-col gap-6 overflow-y-auto pb-24 custom-scrollbar">
          {/* Active Tracker if running */}
          {activeStep !== undefined && (
            <PipelineTracker activeStep={activeStep} />
          )}

          {result ? (
            <div className="space-y-6">
              {/* Hero Stats */}
              <div className="grid grid-cols-3 gap-6">
                
                {/* Circular Gauge */}
                <RiskGauge score={result.riskScore} percentileText={result.percentile} />

                {/* Recommendation Card */}
                <div className="col-span-2 flex flex-col gap-6">
                  <div className="bg-white p-8 rounded-[32px] flex items-center justify-between shadow-soft border border-outline-variant/10">
                    <div>
                      <span className="font-label text-[10px] text-outline-variant font-bold uppercase block mb-1.5 tracking-wider">System Recommendation</span>
                      <div className="flex items-center gap-3">
                        <span 
                          className={`px-6 py-2 rounded-full font-headline text-base font-bold tracking-widest ${
                            result.recommendation === 'APPROVE'
                              ? 'bg-[#ceddc2] text-primary border border-primary/20'
                              : result.recommendation === 'DECLINE'
                              ? 'bg-[#ffdad6] text-[#ba1a1a] border border-[#ba1a1a]/20'
                              : 'bg-[#eae8e4] text-[#444841]'
                          }`}
                        >
                          {result.recommendation}
                        </span>
                        {result.recommendation === 'APPROVE' && (
                          <span className="material-symbols-outlined text-primary text-3xl font-bold">verified</span>
                        )}
                        {result.recommendation === 'DECLINE' && (
                          <span className="material-symbols-outlined text-[#ba1a1a] text-3xl font-bold">cancel</span>
                        )}
                        {result.recommendation === 'MANUAL REVIEW' && (
                          <span className="material-symbols-outlined text-secondary text-3xl font-bold">pending</span>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="font-label text-[10px] text-outline-variant font-bold uppercase block mb-1.5 tracking-wider">AI Confidence</span>
                      <span className="font-headline text-[36px] font-extrabold text-secondary leading-none">{result.confidence}%</span>
                    </div>
                  </div>

                  {/* Cohort Statistics */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-surface-container-low p-4 rounded-2xl flex items-center gap-4 border border-outline-variant/5">
                      <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center text-primary shadow-sm">
                        <span className="material-symbols-outlined font-bold">trending_down</span>
                      </div>
                      <div>
                        <span className="text-[10px] font-label font-bold text-outline uppercase tracking-wider block">Cohort Default</span>
                        <span className="font-headline text-sm font-extrabold text-on-surface">{result.cohortDefaultRate}%</span>
                      </div>
                    </div>
                    <div className="bg-surface-container-low p-4 rounded-2xl flex items-center gap-4 border border-outline-variant/5">
                      <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center text-primary shadow-sm">
                        <span className="material-symbols-outlined font-bold">groups</span>
                      </div>
                      <div>
                        <span className="text-[10px] font-label font-bold text-outline uppercase tracking-wider block">Similar Borrowers</span>
                        <span className="font-headline text-sm font-extrabold text-on-surface">{result.similarBorrowersCount.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Gemini Synthesis Card */}
              <div className="bg-white rounded-[32px] shadow-floating overflow-hidden relative border border-outline-variant/10">
                <div className="h-2 w-full bg-secondary-container"></div>
                <div className="p-8">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-8 bg-secondary-container rounded-full flex items-center justify-center shadow-sm">
                      <span className="material-symbols-outlined text-white text-[16px] font-bold">auto_awesome</span>
                    </div>
                    <h3 className="font-headline text-lg font-bold text-primary">Intelligence Synthesis</h3>
                  </div>

                  <div className="space-y-8 ai-insight-border pl-6">
                    {/* Summary */}
                    <section>
                      <h4 className="font-headline text-sm font-bold text-on-surface mb-2">Summary</h4>
                      <p className="font-body text-sm text-on-surface-variant leading-relaxed font-medium">
                        {result.summary}
                      </p>
                    </section>

                    {/* Key Factors */}
                    <section>
                      <h4 className="font-headline text-sm font-bold text-on-surface mb-3">Key Factors</h4>
                      <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {result.keyFactors.map((factor, index) => (
                          <li key={index} className="flex items-start gap-2">
                            <span 
                              className={`material-symbols-outlined text-[20px] font-bold ${
                                factor.type === 'positive' 
                                  ? 'text-primary' 
                                  : factor.type === 'negative' 
                                  ? 'text-secondary' 
                                  : 'text-outline'
                              }`}
                            >
                              {factor.type === 'positive' ? 'check_circle' : factor.type === 'negative' ? 'cancel' : 'info'}
                            </span>
                            <span className="font-body text-xs text-on-surface-variant">
                              <strong className="font-bold text-on-surface">{factor.label}:</strong> {factor.description}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </section>

                    {/* Supporting Evidence Chart */}
                    <section>
                      <h4 className="font-headline text-sm font-bold text-on-surface mb-3">Supporting Evidence</h4>
                      <div className="bg-surface-container-low rounded-2xl p-6 border border-outline-variant/10">
                        <div className="h-32 w-full mb-4">
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={evidenceData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                              <Bar 
                                dataKey="value" 
                                fill="#55624D" 
                                opacity={0.6}
                                radius={[4, 4, 0, 0]}
                              />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                        <div className="flex justify-between font-label text-[10px] text-outline font-bold uppercase tracking-wider">
                          <span>Q1 2023</span>
                          <span>Credit Velocity Index (Positive Trend)</span>
                          <span>Current</span>
                        </div>
                      </div>
                    </section>

                    {/* Policy Alignment */}
                    <section className="pb-4">
                      <h4 className="font-headline text-sm font-bold text-on-surface mb-2">Policy Alignment</h4>
                      <p className="font-body text-sm text-on-surface-variant leading-relaxed font-medium">
                        {result.policyAlignment}
                      </p>
                    </section>
                  </div>
                </div>
              </div>

              {/* Footer Meta */}
              <div className="flex justify-between items-center px-4 opacity-50 text-[10px] font-label font-bold uppercase tracking-widest">
                <span>Model: Gemini-1.5-Pro</span>
                <span>Scored in {result.scoringTime}s (GPU-accelerated)</span>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center p-12 bg-white rounded-xxl border border-outline-variant/10 shadow-soft h-[350px]">
              <span className="material-symbols-outlined text-[64px] text-outline-variant">analytics</span>
              <p className="mt-4 font-body text-sm font-semibold text-on-surface-variant text-center">
                Fill in the applicant details and click <strong className="text-primary font-bold">Evaluate Application</strong> to trigger decision synthesis.
              </p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
};
