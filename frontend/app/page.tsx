'use client';

import { useState } from 'react';
import { ArrowRight, Github, Loader2, Play, Info, Plus } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  const [repoUrl, setRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ analysis: string; impact: string } | null>(null);

  const analyzeRepo = async () => {
    if (!repoUrl) return;
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl }),
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error('Error analyzing repo:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#141414] text-white font-sans selection:bg-red-600 selection:text-white">

      {/* Navbar */}
      <header className="fixed top-0 w-full z-50 px-4 md:px-12 py-4 bg-gradient-to-b from-black/80 to-transparent transition-all duration-500">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-8">
            <h1 className="text-red-600 text-2xl md:text-3xl font-bold tracking-tighter uppercase">AGENTIC</h1>
            <nav className="hidden md:flex gap-6 text-sm font-medium text-gray-300">
              <a href="#" className="text-white hover:text-gray-300 transition">Dashboard</a>
              <a href="#" className="hover:text-gray-300 transition">Activity</a>
              <a href="#" className="hover:text-gray-300 transition">Settings</a>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/chat" className="text-sm font-medium text-white hover:text-gray-300 transition">
              Agent Chat
            </Link>
            <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center text-xs font-bold">
              DEV
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="relative h-[85vh] w-full flex items-center justify-center md:justify-start">
        {/* Background Image/Gradient */}
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center opacity-20"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-[#141414] via-transparent to-black/40"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/40 to-transparent"></div>

        <div className="relative z-10 px-4 md:px-12 max-w-3xl pt-20 w-full">
          <div className="flex items-center gap-2 mb-4 text-red-600 font-medium tracking-wide uppercase text-sm">
            <Github className="w-4 h-4" />
            <span>Intelligent Analysis</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-black mb-6 tracking-tight leading-none">
            CODE <br /> INTELLIGENCE
          </h1>
          <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-xl drop-shadow-md">
            Deep dive into your repository. AI agents analyze every commit, assessing impact and providing actionable insights for your team.
          </p>

          <div className="flex flex-col md:flex-row gap-4 mb-8 w-full">
            <div className="flex items-center bg-white/10 backdrop-blur-sm border border-white/20 rounded-md overflow-hidden flex-1 max-w-md">
              <input
                type="text"
                placeholder="https://github.com/owner/repo"
                className="bg-transparent border-none text-white placeholder-gray-400 px-4 py-3 w-full focus:ring-0 outline-none"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
              />
            </div>
            <button
              onClick={analyzeRepo}
              disabled={loading}
              className="flex items-center justify-center gap-2 bg-red-600 text-white px-8 py-3 rounded font-bold hover:bg-red-700 transition disabled:opacity-70 whitespace-nowrap"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Play className="w-5 h-5 fill-white" />}
              <span>Analyze</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content Rows */}
      <div className="px-4 md:px-12 pb-20 -mt-20 relative z-20 space-y-12">

        {result && (
          <>
            <div className="space-y-4">
              <h2 className="text-xl md:text-2xl font-semibold text-white hover:text-gray-300 cursor-pointer transition inline-flex items-center gap-2">
                Analysis Report <ArrowRight className="w-4 h-4 text-cyan-500" />
              </h2>
              <div className="bg-[#181818] rounded-md p-6 md:p-8 border border-white/10 hover:border-white/30 transition duration-300 group">
                <div className="prose prose-invert max-w-none">
                  <div className="whitespace-pre-wrap text-gray-300 leading-relaxed group-hover:text-white transition-colors">
                    {result.analysis}
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-xl md:text-2xl font-semibold text-white hover:text-gray-300 cursor-pointer transition inline-flex items-center gap-2">
                Impact Assessment <ArrowRight className="w-4 h-4 text-red-500" />
              </h2>
              <div className="bg-[#181818] rounded-md p-6 md:p-8 border border-white/10 hover:border-white/30 transition duration-300 group">
                <div className="prose prose-invert max-w-none">
                  <div className="whitespace-pre-wrap text-gray-300 leading-relaxed group-hover:text-white transition-colors">
                    {result.impact}
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Placeholder Rows for aesthetic */}
        {!result && (
          <div className="space-y-4 opacity-50 pointer-events-none">
            <h2 className="text-xl font-semibold text-gray-400">Recent Activity</h2>
            <div className="flex gap-4 overflow-x-hidden">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="min-w-[250px] h-[140px] bg-[#2f2f2f] rounded-md animate-pulse"></div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
