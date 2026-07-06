import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { HistoryService } from '../services/api';

export const History: React.FC = () => {
  const { data: historyItems, isLoading } = useQuery({
    queryKey: ['applicantHistory'],
    queryFn: HistoryService.list,
  });

  const [expandedRows, setExpandedRows] = useState<Record<string, boolean>>({});

  const toggleRow = (id: string) => {
    setExpandedRows(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  if (isLoading || !historyItems) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-100px)]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-[1400px] mx-auto space-y-8">
      {/* Page Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h2 className="font-headline text-[36px] font-bold text-primary">Applicant History</h2>
          <p className="text-on-surface-variant font-body text-sm font-semibold">Review historical decisions and AI-driven risk justifications across the enterprise portfolio.</p>
        </div>
        <div className="flex space-x-3">
          <button className="px-4 py-2 bg-surface-container-high hover:bg-primary-fixed rounded-lg text-primary font-label text-xs uppercase tracking-wider font-bold flex items-center space-x-2 transition-colors duration-150 outline-none">
            <span className="material-symbols-outlined text-[18px]">file_download</span>
            <span>Export CSV</span>
          </button>
        </div>
      </section>

      {/* Search & Filters Bento */}
      <section className="bg-white rounded-xxl p-6 shadow-soft border border-outline-variant/10">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div>
            <label className="block text-[11px] font-label font-bold text-outline uppercase tracking-wider mb-1">Risk Profile</label>
            <select className="w-full bg-surface-container-low border-none rounded-xl text-xs font-body font-semibold px-3 py-2.5 outline-none focus:ring-1 focus:ring-primary">
              <option>All Risk Levels</option>
              <option>Low Risk</option>
              <option>Moderate</option>
              <option>Elevated</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-label font-bold text-outline uppercase tracking-wider mb-1">Decision</label>
            <select className="w-full bg-surface-container-low border-none rounded-xl text-xs font-body font-semibold px-3 py-2.5 outline-none focus:ring-1 focus:ring-primary">
              <option>Any Status</option>
              <option>Approved</option>
              <option>Declined</option>
              <option>In Review</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-label font-bold text-outline uppercase tracking-wider mb-1">Loan Range</label>
            <div className="flex items-center space-x-2">
              <input className="w-1/2 bg-surface-container-low border-none rounded-xl text-xs font-body font-semibold px-3 py-2.5 outline-none focus:ring-1 focus:ring-primary" placeholder="$0" type="text" />
              <span className="text-xs text-outline font-semibold">to</span>
              <input className="w-1/2 bg-surface-container-low border-none rounded-xl text-xs font-body font-semibold px-3 py-2.5 outline-none focus:ring-1 focus:ring-primary" placeholder="$1M+" type="text" />
            </div>
          </div>
          <div>
            <label className="block text-[11px] font-label font-bold text-outline uppercase tracking-wider mb-1">Date Range</label>
            <button className="w-full bg-surface-container-low border-none rounded-xl text-xs font-body font-semibold px-4 py-2.5 text-left text-on-surface-variant flex justify-between items-center outline-none">
              <span>Last 30 Days</span>
              <span className="material-symbols-outlined text-[16px] text-outline">calendar_today</span>
            </button>
          </div>
          <div className="flex items-end">
            <button className="w-full bg-primary-container hover:brightness-110 text-white rounded-xl py-2.5 font-label text-xs uppercase tracking-wider font-bold transition-all outline-none">
              Apply Filters
            </button>
          </div>
        </div>
      </section>

      {/* History Table Container */}
      <section className="bg-white rounded-[24px] shadow-soft overflow-hidden border border-outline-variant/10">
        <div className="overflow-x-auto custom-scrollbar">
          <table className="w-full border-collapse">
            <thead className="sticky top-0 bg-surface-container-low z-10 border-b border-outline-variant/10">
              <tr className="text-left">
                <th className="px-8 py-4 font-label text-xs text-outline uppercase tracking-widest w-16"></th>
                <th className="px-4 py-4 font-label text-xs text-outline uppercase tracking-widest">Applicant</th>
                <th className="px-4 py-4 font-label text-xs text-outline uppercase tracking-widest">Amount</th>
                <th className="px-4 py-4 font-label text-xs text-outline uppercase tracking-widest">Risk Level</th>
                <th className="px-4 py-4 font-label text-xs text-outline uppercase tracking-widest">Decision</th>
                <th className="px-4 py-4 font-label text-xs text-outline uppercase tracking-widest">Processed</th>
                <th className="px-8 py-4 font-label text-xs text-outline uppercase tracking-widest text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-container">
              {historyItems.map((item, index) => {
                const isExpanded = !!expandedRows[item.id];
                
                // Color mapping for Risk Level badges
                let riskBadgeClass = "px-3 py-1 rounded-full text-[11px] font-label font-bold border ";
                if (item.riskLevel === 'Low Risk') {
                  riskBadgeClass += "bg-green-50 text-green-700 border-green-100";
                } else if (item.riskLevel === 'Moderate') {
                  riskBadgeClass += "bg-yellow-50 text-yellow-700 border-yellow-100";
                } else {
                  riskBadgeClass += "bg-red-50 text-red-700 border-red-100";
                }

                // Color mapping for Decision status text
                let decisionTextClass = "flex items-center font-bold text-sm ";
                let decisionIcon = "pending";
                if (item.decision === 'Approved') {
                  decisionTextClass += "text-green-600";
                  decisionIcon = "check_circle";
                } else if (item.decision === 'Declined') {
                  decisionTextClass += "text-red-600";
                  decisionIcon = "cancel";
                } else {
                  decisionTextClass += "text-[#fd7e65]";
                  decisionIcon = "pending";
                }

                return (
                  <React.Fragment key={item.id}>
                    {/* Primary Row */}
                    <tr 
                      className={`hover:bg-surface-container-low transition-colors duration-150 cursor-pointer ${
                        index % 2 !== 0 ? 'bg-surface-container-lowest' : ''
                      }`} 
                      onClick={() => toggleRow(item.id)}
                    >
                      <td className="px-8 py-6 text-center">
                        <span 
                          className="material-symbols-outlined text-outline transition-transform duration-300 text-[20px]"
                          style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
                        >
                          expand_more
                        </span>
                      </td>
                      <td className="px-4 py-6">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 rounded-full bg-primary-fixed flex items-center justify-center text-primary font-bold text-xs">
                            {item.name.split(' ').map(n => n[0]).join('')}
                          </div>
                          <div>
                            <p className="font-bold text-on-surface text-sm">{item.name}</p>
                            <p className="text-[10px] text-outline font-semibold uppercase tracking-wider">{item.type}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-6 font-headline text-sm font-bold text-on-surface">
                        ${item.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-6">
                        <span className={riskBadgeClass}>{item.riskLevel}</span>
                      </td>
                      <td className="px-4 py-6">
                        <span className={decisionTextClass}>
                          <span className="material-symbols-outlined text-[18px] mr-1">{decisionIcon}</span>
                          {item.decision}
                        </span>
                      </td>
                      <td className="px-4 py-6 text-xs font-body font-semibold text-on-surface-variant">
                        {item.processedDate}
                      </td>
                      <td className="px-8 py-6 text-right">
                        <button 
                          className="text-primary hover:underline text-xs font-bold uppercase tracking-wider"
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleRow(item.id);
                          }}
                        >
                          {isExpanded ? 'Hide Details' : 'View Details'}
                        </button>
                      </td>
                    </tr>

                    {/* Expanded Detail Row */}
                    {isExpanded && item.expandedDetails && (
                      <tr className="bg-surface-container-low/40">
                        <td className="px-8" colSpan={7}>
                          <div className="py-8 space-y-8 max-w-6xl">
                            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                              
                              {/* AI Explanation Box */}
                              <div className="lg:col-span-2 bg-white rounded-2xl p-6 ai-insight-border shadow-sm border border-outline-variant/10">
                                <div className="flex items-center space-x-2 mb-4 text-secondary">
                                  <span className="material-symbols-outlined font-bold text-[20px]">auto_awesome</span>
                                  <h4 className="font-headline text-sm font-bold text-on-surface">Gemini Decision Analysis</h4>
                                </div>
                                <p className="font-body text-xs text-on-surface-variant leading-relaxed font-semibold">
                                  {item.expandedDetails.summary}
                                </p>
                                <div className="mt-6 flex flex-wrap gap-2">
                                  <span className="px-3 py-1 bg-surface-container-low border border-outline-variant/20 rounded text-[10px] font-label font-bold text-on-surface-variant uppercase tracking-wider">
                                    LTV: {item.expandedDetails.ltv}%
                                  </span>
                                  <span className="px-3 py-1 bg-surface-container-low border border-outline-variant/20 rounded text-[10px] font-label font-bold text-on-surface-variant uppercase tracking-wider">
                                    DTI: {item.expandedDetails.dti}%
                                  </span>
                                  <span className="px-3 py-1 bg-surface-container-low border border-outline-variant/20 rounded text-[10px] font-label font-bold text-on-surface-variant uppercase tracking-wider">
                                    FICO: {item.expandedDetails.fico}
                                  </span>
                                </div>
                              </div>

                              {/* Risk Factors */}
                              <div className="bg-white rounded-2xl p-6 shadow-sm border border-outline-variant/10">
                                <h4 className="font-headline text-sm font-bold text-on-surface mb-4">Risk Factors</h4>
                                <ul className="space-y-3">
                                  {item.expandedDetails.factors.map((factor, idx) => (
                                    <li key={idx} className="flex items-start space-x-2">
                                      <span 
                                        className={`material-symbols-outlined text-[18px] font-bold ${
                                          factor.type === 'success' 
                                            ? 'text-primary' 
                                            : factor.type === 'warning' 
                                            ? 'text-secondary' 
                                            : 'text-outline-variant'
                                        }`}
                                      >
                                        {factor.type === 'success' ? 'check_circle' : factor.type === 'warning' ? 'warning' : 'info'}
                                      </span>
                                      <span className="font-body text-xs font-semibold text-on-surface-variant">
                                        {factor.label}
                                      </span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>

                            {/* Timeline */}
                            <div className="bg-white rounded-2xl p-6 shadow-sm border border-outline-variant/10">
                              <h4 className="font-headline text-sm font-bold text-on-surface mb-6">Decision Timeline</h4>
                              <div className="relative flex justify-between items-start">
                                <div className="absolute top-4 left-0 w-full h-[2px] bg-surface-container-highest -z-0"></div>
                                {item.expandedDetails.timeline.map((step, idx) => (
                                  <div key={idx} className="relative z-10 flex flex-col items-center text-center w-1/4">
                                    <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center mb-2 font-headline text-xs font-bold shadow-sm">
                                      {step.label === 'Final Approval' || step.label === 'Policy Reject' ? (
                                        <span className="material-symbols-outlined text-[14px] font-bold">check</span>
                                      ) : (
                                        step.step
                                      )}
                                    </div>
                                    <p className="font-body text-xs font-bold text-on-surface">{step.label}</p>
                                    <p className="text-[10px] font-label text-outline font-semibold tracking-wider mt-0.5">{step.time}</p>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Table Footer / Pagination */}
        <div className="px-8 py-4 bg-white border-t border-surface-container flex items-center justify-between">
          <p className="text-xs font-body font-semibold text-outline">
            Showing {historyItems.length} of 1,248 historical applications
          </p>
          <div className="flex space-x-2">
            <button className="p-2 rounded-lg border border-outline-variant/40 hover:bg-surface-container transition-colors outline-none">
              <span className="material-symbols-outlined text-[18px]">chevron_left</span>
            </button>
            <button className="w-8 h-8 rounded-lg border border-outline-variant/40 bg-primary text-white transition-colors text-xs font-bold outline-none">1</button>
            <button className="w-8 h-8 rounded-lg border border-outline-variant/40 hover:bg-surface-container transition-colors text-xs font-bold outline-none">2</button>
            <button className="w-8 h-8 rounded-lg border border-outline-variant/40 hover:bg-surface-container transition-colors text-xs font-bold outline-none">3</button>
            <button className="p-2 rounded-lg border border-outline-variant/40 hover:bg-surface-container transition-colors outline-none">
              <span className="material-symbols-outlined text-[18px]">chevron_right</span>
            </button>
          </div>
        </div>
      </section>

      {/* Bottom Status Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-[24px] shadow-soft border border-outline-variant/10 flex items-center space-x-4">
          <div className="w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center text-primary">
            <span className="material-symbols-outlined text-[24px] font-bold">verified</span>
          </div>
          <div>
            <p className="text-[10px] font-label font-bold text-outline uppercase tracking-wider">Approval Rate</p>
            <p className="font-headline text-[24px] font-extrabold leading-tight text-primary">74.2%</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-[24px] shadow-soft border border-outline-variant/10 flex items-center space-x-4">
          <div className="w-12 h-12 rounded-full bg-secondary-fixed flex items-center justify-center text-secondary">
            <span className="material-symbols-outlined text-[24px] font-bold">warning</span>
          </div>
          <div>
            <p className="text-[10px] font-label font-bold text-outline uppercase tracking-wider">Avg Risk Score</p>
            <p className="font-headline text-[24px] font-extrabold leading-tight text-secondary">312</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-[24px] shadow-soft border border-outline-variant/10 flex items-center space-x-4">
          <div className="w-12 h-12 rounded-full bg-tertiary-fixed flex items-center justify-center text-tertiary">
            <span className="material-symbols-outlined text-[24px] font-bold">timer</span>
          </div>
          <div>
            <p className="text-[10px] font-label font-bold text-outline uppercase tracking-wider">Avg Process Time</p>
            <p className="font-headline text-[24px] font-extrabold leading-tight text-tertiary">1.4 Days</p>
          </div>
        </div>
      </section>
    </div>
  );
};
