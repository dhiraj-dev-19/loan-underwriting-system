export interface ApplicantDetails {
  name: string;
  dob: string;
  ssn: string;
  employer: string;
  income: number; // Monthly or Annual depending on input. We will accept annual and convert, or monthly.
  tenure: number;
  fico: number;
  dti: number; // DTI ratio percentage e.g. 22
  outstandingDebt: string;
  requestedAmount: number;
  term: string;
  // Raw fields used by the original Streamlit model interface:
  monthlyIncome?: number;
  debtRatio?: number;
  creditLines?: number;
  delinquencies?: number;
  dependents?: number;
}

export interface UnderwritingResult {
  applicationId: string;
  applicant: ApplicantDetails;
  riskScore: number; // 0 to 1000 or 0 to 1
  percentile: string;
  recommendation: 'APPROVE' | 'MANUAL REVIEW' | 'DECLINE';
  confidence: number; // Percentage
  cohortDefaultRate: number; // Percentage
  similarBorrowersCount: number;
  summary: string;
  keyFactors: Array<{
    type: 'positive' | 'negative' | 'neutral';
    label: string;
    description: string;
  }>;
  policyAlignment: string;
  scoringTime: number; // seconds
}

export interface HistoryItem {
  id: string;
  name: string;
  type: string;
  amount: number;
  riskLevel: 'Low Risk' | 'Moderate' | 'Elevated';
  decision: 'Approved' | 'Declined' | 'In Review';
  processedDate: string;
  expandedDetails?: {
    summary: string;
    ltv: number;
    dti: number;
    fico: number;
    factors: Array<{
      type: 'success' | 'info' | 'warning';
      label: string;
    }>;
    timeline: Array<{
      step: number;
      label: string;
      time: string;
    }>;
  };
}

export interface DashboardSummary {
  processedCount: number;
  approvalRate: number; // percentage
  avgRiskScore: number;
  pendingReviewsCount: number;
  recentApplications: Array<{
    initials: string;
    name: string;
    amount: number;
    riskScoreText: string;
    riskScoreColor: string; // e.g. 'primary' | 'secondary' | 'error'
    recommendation: string;
    recommendationColor: string;
    status: string;
    statusColor: string;
  }>;
  recentDecisions: Array<{
    id: string;
    name: string;
    loanType: string;
    recommendation: 'APPROVE' | 'FLAG' | 'DECLINE';
    confidence: number;
    insight: string;
    time: string;
  }>;
  riskDistribution: {
    lowRisk: number;
    medRisk: number;
    highRisk: number;
  };
  approvalTrends: Array<{
    day: string;
    value: number;
    active?: boolean;
  }>;
}
