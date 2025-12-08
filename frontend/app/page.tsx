'use client';
import { useState } from "react";
import { Shield, TrendingUp, AlertTriangle, CheckCircle, Code, Zap } from "lucide-react";

type ScoreResult = {
  risk_class: string;
  default_probability: number;
  emoji: string;
  recommendation: string;
  features: Record<string, number>;
};

export default function Home() {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
  const [mode, setMode] = useState('simple'); // 'simple' or 'advanced'
  const [profile, setProfile] = useState('good_spender');
  const [customJson, setCustomJson] = useState(JSON.stringify({
    "transactions": [
      {
        "date": "2025-06-01T00:00:00",
        "amount": 800,
        "type": "income"
      },
      {
        "date": "2025-06-05T00:00:00",
        "amount": 200,
        "type": "expense",
        "category": "groceries"
      }
    ],
    "repayments": [
      {
        "loan_id": "LOAN-1",
        "status": "on_time"
      }
    ]
  }, null, 2));
  const [result, setResult] = useState<ScoreResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submitSimple() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      if (err instanceof Error) {
        setError('Error: ' + err.message);
      } else {
        setError("Unknown error");
      }
    }
    setLoading(false);
  }

  async function submitAdvanced() {
    setLoading(true);
    setError(null);
    try {
      const parsed = JSON.parse(customJson);
      const res = await fetch(`${API_BASE_URL}/score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(parsed)
      });
      const data = await res.json();
      console.log(data);
      setResult(data.result || data);
    } catch (err) {
      if (err instanceof Error) {
        setError('Error: ' + err.message);
      } else {
        setError("Unknown error");
      }
    }
    setLoading(false);
  }

  const getRiskColor = () => {
    if (!result) return 'bg-gray-100';
    const risk = result.risk_class?.toLowerCase();
    if (risk === 'low risk') return 'bg-green-100 text-green-800 border-green-300';
    if (risk === 'medium risk') return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    return 'bg-red-100 text-red-800 border-red-300';
  };

  const getRiskIcon = () => {
    if (!result) return null;
    const risk = result.risk_class?.toLowerCase();
    if (risk === 'low risk') return <CheckCircle className="w-6 h-6 text-green-600" />;
    if (risk === 'medium risk') return <AlertTriangle className="w-6 h-6 text-yellow-600" />;
    return <AlertTriangle className="w-6 h-6 text-red-600" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Shield className="w-12 h-12 text-indigo-600" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              LoanGuard AI
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Intelligent Risk Scoring for Smarter Lending Decisions</p>
        </div>

        {/* Mode Toggle */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-xl shadow-lg p-1 inline-flex">
            <button
              onClick={() => { setMode('simple'); setResult(null); setError(null); }}
              className={`px-6 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                mode === 'simple' 
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md' 
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <Zap className="w-5 h-5" />
              Quick Demo
            </button>
            <button
              onClick={() => { setMode('advanced'); setResult(null); setError(null); }}
              className={`px-6 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                mode === 'advanced' 
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md' 
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <Code className="w-5 h-5" />
              Custom JSON
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Panel */}
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-6">
              <h2 className="text-2xl font-semibold text-white flex items-center gap-2">
                <TrendingUp className="w-6 h-6" />
                {mode === 'simple' ? 'Profile Selection' : 'Custom Data Input'}
              </h2>
            </div>

            <div className="p-8 space-y-6">
              {mode === 'simple' ? (
                <>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Select Borrower Profile
                    </label>
                    <select
                      value={profile}
                      onChange={(e) => setProfile(e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-gray-700 font-medium"
                    >
                      <option value="good_spender">Good Spender</option>
                      <option value="gambling_spender">Gambling Spender</option>
                      <option value="inconsistent_earner">Inconsistent Earner</option>
                    </select>
                  </div>

                  <button
                    onClick={submitSimple}
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Analyzing...' : 'Score Borrower'}
                  </button>
                </>
              ) : (
                <>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Transaction & Repayment Data (JSON)
                    </label>
                    <textarea
                      value={customJson}
                      onChange={(e) => setCustomJson(e.target.value)}
                      className="w-full h-96 px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-gray-700 font-mono text-sm"
                      placeholder="Enter JSON data..."
                    />
                  </div>

                  <button
                    onClick={submitAdvanced}
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Processing...' : 'Analyze Custom Data'}
                  </button>
                </>
              )}

              {error && (
                <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
                  <p className="text-red-800 text-sm font-medium">{error}</p>
                </div>
              )}
            </div>
          </div>

          {/* Results Panel */}
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-6">
              <h2 className="text-2xl font-semibold text-white">Risk Assessment Results</h2>
            </div>

            <div className="p-8">
              {!result ? (
                <div className="h-full flex items-center justify-center text-gray-400 text-center py-20">
                  <div>
                    <Shield className="w-20 h-20 mx-auto mb-4 opacity-20" />
                    <p className="text-lg font-medium">No results yet</p>
                    <p className="text-sm mt-2">Submit a profile or custom data to see risk analysis</p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4 animate-in fade-in duration-500">
                  <div className="h-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full"></div>
                  
                  {/* Risk Class */}
                  <div className={`border-2 rounded-xl p-6 ${getRiskColor()} transition-all`}>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold opacity-75 mb-1">Risk Classification</p>
                        <p className="text-3xl font-bold">{result.risk_class}</p>
                      </div>
                      {getRiskIcon()}
                    </div>
                  </div>

                  {/* Default Probability */}
                  <div className="bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-gray-200 rounded-xl p-6">
                    <p className="text-sm font-semibold text-gray-600 mb-2">Default Probability</p>
                    <div className="flex items-end gap-2">
                      <p className="text-4xl font-bold text-gray-800">{(result?.default_probability ?? 0).toFixed(2)}%</p>
                    </div>
                    <div className="mt-3 bg-gray-200 rounded-full h-3 overflow-hidden">
                      <div 
                        className="bg-gradient-to-r from-indigo-600 to-purple-600 h-full transition-all duration-700"
                        style={{ width: `${Math.min(result.default_probability, 100)}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Recommendation */}
                  <div className="bg-indigo-50 border-2 border-indigo-200 rounded-xl p-6">
                    <p className="text-sm font-semibold text-indigo-900 mb-2">Recommendation</p>
                    <p className="text-lg text-indigo-800 leading-relaxed">{result.recommendation}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          Powered by Machine Learning • Real-time Risk Assessment
        </div>
      </div>
    </div>
  );
}
