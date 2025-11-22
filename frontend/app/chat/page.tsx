'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, ArrowLeft, Play } from 'lucide-react';
import Link from 'next/link';

export default function Chat() {
    const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || loading) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const res = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!res.ok) throw new Error('Failed to send message');

            const data = await res.json();
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, { role: 'assistant', content: "I'm sorry, I encountered an error connecting to the agent. Please ensure the backend is running." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#141414] text-white font-sans flex flex-col">

            {/* Header */}
            <header className="px-4 md:px-8 py-4 bg-black/50 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="text-gray-400 hover:text-white transition">
                            <ArrowLeft className="w-6 h-6" />
                        </Link>
                        <div>
                            <h1 className="text-lg font-bold">Agentic Planner</h1>
                            <p className="text-xs text-gray-400">Project Coordination & Task Planning</p>
                        </div>
                    </div>
                    <div className="text-red-600 font-bold tracking-widest text-sm">AGENTIC</div>
                </div>
            </header>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-center opacity-50">
                        <div className="w-20 h-20 rounded-full border-2 border-gray-600 flex items-center justify-center mb-4">
                            <Play className="w-8 h-8 fill-white text-white ml-1" />
                        </div>
                        <h2 className="text-xl font-bold mb-2">Start the Conversation</h2>
                        <p className="text-sm text-gray-400">Ask about your project plan or recent commits.</p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''} animate-in fade-in slide-in-from-bottom-4 duration-300`}
                    >
                        <div className={`w-10 h-10 rounded flex items-center justify-center flex-shrink-0 font-bold text-sm ${msg.role === 'user'
                            ? 'bg-blue-600'
                            : 'bg-red-600'
                            }`}>
                            {msg.role === 'user' ? 'YOU' : 'AI'}
                        </div>

                        <div className={`max-w-[80%] rounded p-4 ${msg.role === 'user'
                            ? 'bg-[#2f2f2f] text-white'
                            : 'bg-black border border-white/20 text-gray-200'
                            }`}>
                            <p className="leading-relaxed whitespace-pre-wrap text-sm md:text-base">{msg.content}</p>
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex gap-4 animate-in fade-in slide-in-from-bottom-4">
                        <div className="w-10 h-10 rounded bg-red-600 flex items-center justify-center flex-shrink-0 font-bold text-sm">
                            AI
                        </div>
                        <div className="bg-black border border-white/20 rounded p-4 flex items-center gap-2">
                            <span className="w-1.5 h-1.5 bg-red-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                            <span className="w-1.5 h-1.5 bg-red-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                            <span className="w-1.5 h-1.5 bg-red-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 md:p-6 bg-[#141414] border-t border-white/10">
                <div className="max-w-4xl mx-auto relative">
                    <input
                        type="text"
                        placeholder="Type your message..."
                        className="w-full bg-[#2f2f2f] text-white rounded px-6 py-4 pr-16 focus:outline-none focus:ring-2 focus:ring-white/20 placeholder-gray-500"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                        disabled={loading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={loading || !input.trim()}
                        className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white p-2 transition disabled:opacity-50"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </div>
    );
}
