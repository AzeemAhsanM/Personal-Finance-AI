import React, { useState, useEffect } from 'react';
import './calculator.css';

const Calculator = () => {
  const [activeCalculator, setActiveCalculator] = useState('sip'); // 'sip' or 'emi'

  // State for SIP Calculator
  const [sipAmount, setSipAmount] = useState(5000);
  const [sipRate, setSipRate] = useState(12);
  const [sipYears, setSipYears] = useState(10);
  const [sipResult, setSipResult] = useState({ invested: 0, returns: 0, total: 0 });

  // State for EMI Calculator
  const [emiAmount, setEmiAmount] = useState(1000000);
  const [emiRate, setEmiRate] = useState(8.5);
  const [emiMonths, setEmiMonths] = useState(120);
  const [emiResult, setEmiResult] = useState({ monthlyEmi: 0, principal: 0, interest: 0, total: 0 });

  // Calculate SIP whenever its inputs change
  useEffect(() => {
    const i = (sipRate / 100) / 12; // Monthly interest rate
    const n = sipYears * 12; // Number of months
    const M = sipAmount * ((Math.pow(1 + i, n) - 1) / i) * (1 + i);
    
    const totalInvested = sipAmount * n;
    const wealthGained = M - totalInvested;

    setSipResult({
      invested: totalInvested.toFixed(0),
      returns: wealthGained.toFixed(0),
      total: M.toFixed(0),
    });
  }, [sipAmount, sipRate, sipYears]);

  // Calculate EMI whenever its inputs change
  useEffect(() => {
    const P = emiAmount;
    const r = (emiRate / 100) / 12; // Monthly interest rate
    const n = emiMonths;
    if (r > 0) {
        const emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
        const totalPayable = emi * n;
        const totalInterest = totalPayable - P;
        setEmiResult({
            monthlyEmi: emi.toFixed(0),
            principal: P.toFixed(0),
            interest: totalInterest.toFixed(0),
            total: totalPayable.toFixed(0),
        });
    }
  }, [emiAmount, emiRate, emiMonths]);

  return (
    <div className="calculator-page-container">
      <div className="calculator-card">
        <div className="calculator-toggle">
          <button onClick={() => setActiveCalculator('sip')} className={activeCalculator === 'sip' ? 'active' : ''}>SIP Calculator</button>
          <button onClick={() => setActiveCalculator('emi')} className={activeCalculator === 'emi' ? 'active' : ''}>EMI Calculator</button>
        </div>

        {activeCalculator === 'sip' && (
          <div className="calculator-content">
            {/* SIP Inputs */}
            <div className="form-group-calc">
              <label>Monthly Investment: ₹{Number(sipAmount).toLocaleString('en-IN')}</label>
              <input type="range" min="100" max="100000" step="500" value={sipAmount} onChange={(e) => setSipAmount(e.target.value)} />
            </div>
            <div className="form-group-calc">
              <label>Expected Return Rate (% p.a.): {sipRate}%</label>
              <input type="range" min="1" max="30" step="0.5" value={sipRate} onChange={(e) => setSipRate(e.target.value)} />
            </div>
            <div className="form-group-calc">
              <label>Time Period (Years): {sipYears}</label>
              <input type="range" min="1" max="40" value={sipYears} onChange={(e) => setSipYears(e.target.value)} />
            </div>
            
            {/* SIP Results */}
            <div className="result-section">
              <p>Invested Amount: <span>₹{Number(sipResult.invested).toLocaleString('en-IN')}</span></p>
              <p>Est. Returns: <span>₹{Number(sipResult.returns).toLocaleString('en-IN')}</span></p>
              <p className="total-value">Total Value: <span>₹{Number(sipResult.total).toLocaleString('en-IN')}</span></p>
            </div>
          </div>
        )}

        {activeCalculator === 'emi' && (
          <div className="calculator-content">
            {/* EMI Inputs */}
            <div className="form-group-calc">
                <label>Loan Amount: ₹{Number(emiAmount).toLocaleString('en-IN')}</label>
                <input type="range" min="10000" max="10000000" step="10000" value={emiAmount} onChange={(e) => setEmiAmount(e.target.value)} />
            </div>
            <div className="form-group-calc">
                <label>Interest Rate: {emiRate}%</label>
                <input type="range" min="0" max="20" step="0.1" value={emiRate} onChange={(e) => setEmiRate(e.target.value)} />
            </div>
            <div className="form-group-calc">
                <label>Loan Tenure (Months): {emiMonths}</label>
                <input type="range" min="1" max="360" value={emiMonths} onChange={(e) => setEmiMonths(e.target.value)} />
            </div>

            {/* EMI Results */}
            <div className="result-section">
                <p>Principal Amount: <span>₹{Number(emiResult.principal).toLocaleString('en-IN')}</span></p>
                <p>Total Interest: <span>₹{Number(emiResult.interest).toLocaleString('en-IN')}</span></p>
                <p>Total Payable: <span>₹{Number(emiResult.total).toLocaleString('en-IN')}</span></p>
                <p className="total-value">Monthly EMI: <span>₹{Number(emiResult.monthlyEmi).toLocaleString('en-IN')}</span></p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Calculator;