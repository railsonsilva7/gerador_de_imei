"use client";

import { useState, useEffect } from "react";
import { Copy, CheckCircle2, Loader2, Smartphone, ShieldCheck, RefreshCw } from "lucide-react";

export default function Home() {
  const [imei, setImei] = useState<string | null>(null);
  const [prefix, setPrefix] = useState<string>("35390744");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (copied) {
      const timeout = setTimeout(() => setCopied(false), 2000);
      return () => clearTimeout(timeout);
    }
  }, [copied]);

  const generateImei = async () => {
    if (!prefix || prefix.length !== 8 || !/^\d+$/.test(prefix)) {
      setError("O prefixo deve conter exatamente 8 dígitos numéricos.");
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "https://geradorimei.discloud.app/generate";
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ prefix: prefix, quantity: 1 })
      });
      
      if (!response.ok) {
        throw new Error(`Erro ${response.status}: Prefixo inválido ou bloqueio de requisições`);
      }
      
      const data = await response.json();
      if (data && data.imeis && data.imeis.length > 0) {
        setImei(data.imeis[0]);
      } else {
        throw new Error("Estrutura de dados retornada inválida");
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Não foi possível gerar o IMEI. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (imei) {
      navigator.clipboard.writeText(imei);
      setCopied(true);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-200 dark:from-slate-900 dark:to-slate-950 flex flex-col items-center justify-center p-6 relative overflow-hidden">
      
      {/* Background Decorativo */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-500/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-500/20 rounded-full blur-[120px] pointer-events-none" />

      {/* Main Container */}
      <div className="z-10 w-full max-w-lg">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center p-3 sm:p-4 bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 mb-6 relative">
             <Smartphone className="w-8 h-8 sm:w-10 sm:h-10 text-indigo-600 dark:text-indigo-400" />
             <div className="absolute -top-2 -right-2 bg-emerald-500 rounded-full p-1 border-2 border-white dark:border-slate-800">
               <ShieldCheck className="w-4 h-4 text-white" />
             </div>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-800 dark:text-slate-100 tracking-tight mb-3">
            Gerador de IMEI
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm sm:text-base font-medium max-w-sm mx-auto">
            Deseja gerar um código IMEI válido instantaneamente?
          </p>
        </div>

        {/* Card de Ação (Glassmorphism) */}
        <div className="bg-white/70 dark:bg-slate-800/80 backdrop-blur-xl border border-white/50 dark:border-slate-700/50 p-6 sm:p-8 rounded-3xl shadow-2xl">
          
          <div className="mb-4">
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Prefixo de IMEI (8 dígitos)</label>
            <input 
              type="text" 
              maxLength={8}
              value={prefix}
              onChange={(e) => setPrefix(e.target.value.replace(/\D/g, ''))}
              placeholder="Ex: 35390744"
              className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg px-4 py-3 text-slate-800 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all font-mono"
            />
          </div>

          <button
            onClick={generateImei}
            disabled={loading || prefix.length !== 8}
            className="group relative w-full flex items-center justify-center gap-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 dark:disabled:bg-indigo-800 text-white font-semibold py-4 rounded-xl transition-all duration-300 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-indigo-500/30 overflow-hidden active:scale-[0.98]"
          >
            {loading ? (
              <Loader2 className="w-6 h-6 animate-spin text-indigo-100" />
            ) : (
              <>
                <RefreshCw className="w-5 h-5 transition-transform group-hover:rotate-180 duration-500" />
                <span>Gerar Novo IMEI</span>
              </>
            )}
          </button>
          
          {error && (
            <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm font-medium rounded-lg text-center border border-red-100 dark:border-red-900/50">
              {error}
            </div>
          )}

          {/* Resultado */}
          <div className={`mt-6 transition-all duration-500 ease-out overflow-hidden origin-top ${imei ? 'opacity-100 scale-y-100 max-h-32' : 'opacity-0 scale-y-0 max-h-0'}`}>
            <div className="p-1 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500">
              <div className="bg-white dark:bg-slate-900 rounded-lg p-4 flex items-center justify-between group">
                <div className="flex flex-col">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Resultado</span>
                  <code className="text-xl sm:text-2xl font-mono font-bold tracking-widest text-slate-800 dark:text-slate-100 selection:bg-indigo-200 dark:selection:bg-indigo-900">
                    {imei}
                  </code>
                </div>
                
                <button
                  onClick={handleCopy}
                  className="p-3 bg-slate-100 dark:bg-slate-800 rounded-lg hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition-colors text-slate-600 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 group/btn relative"
                  aria-label="Copiar"
                >
                  {copied ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                  ) : (
                    <Copy className="w-6 h-6" />
                  )}
                  {/* Tooltip */}
                  <span className="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-800 dark:bg-white text-white dark:text-slate-800 text-xs font-bold py-1 px-2 rounded opacity-0 group-hover/btn:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                    {copied ? 'Copiado!' : 'Copiar'}
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Footer info */}
        <p className="text-center text-slate-400 dark:text-slate-500 text-xs mt-8">
          Desenvolvido com foco em performance e segurança.
        </p>
      </div>
    </main>
  );
}
