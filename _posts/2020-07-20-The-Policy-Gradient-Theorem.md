
\begin{equation}
V(s) =\sum \pi(a \mid s) Q(s, a) \\
\end{equation}

\begin{equation}
Q(s, a) =\sum_{s^{\prime}, r^{\prime}} p\left(s^{\prime}, r^{\prime} \mid s, a\right)\left(r^{\prime}+V\left(s^{\prime}\right)\right) \\
\end{equation}

\begin{equation}
J(\theta) =V\left(S_{0}\right)
\end{equation}

\begin{equation}
\nabla_{\theta} V(s)=\nabla_{\theta} \sum_a \pi(a \mid s) Q(s, a)
\end{equation}

\begin{equation}
\nabla_{\theta} V(s)=\sum_{a} \nabla_{\theta} \pi(a \mid s) Q(s, a)+\pi(a \mid s) \nabla_{\theta} Q(s, a) 
\end{equation}

\begin{equation}
Q(s, a)=\sum_{s^{\prime}, r^{\prime}} p\left(s^{\prime}, r^{\prime} \mid s, a\right) r+\sum_{s^{\prime}, r^{\prime}} p\left(s^{\prime}, r^{\prime} \mid s, a\right) V\left(s^{\prime}\right) 
\end{equation}

\begin{equation}
\nabla_{\theta} Q(s, a)= \nabla_{\theta} \sum_{s^{\prime}, r^{\prime}} p\left(s^{\prime}, r^{\prime} \mid s, a\right) r+ \nabla_{\theta} \sum_{s^{\prime}, r^{\prime}} p\left(s^{\prime}, r^{\prime} \mid s, a\right) V\left(s^{\prime}\right) 
\end{equation}

\begin{equation}
\nabla_{\theta} Q(s, a)= \nabla_{\theta} \sum_{s^{\prime}, r^{\prime}} p\left(s^{\prime}, r^{\prime} \mid s, a\right) V\left(s^{\prime}\right) 
\end{equation}

\begin{equation}
\nabla_{\theta} Q(s, a)=\nabla_{\theta} \sum_{s^{\prime}} p\left(s^{\prime} \mid s, a\right) V\left(s^{\prime}\right)
\end{equation}

\begin{equation}
\nabla_{\theta} Q(s, a)= \sum_{s^{\prime}} p\left(s^{\prime} \mid s, a\right) \nabla_{\theta} V\left(s^{\prime}\right)
\end{equation}

\begin{equation}
\nabla_{\theta} V(s)=\sum_{a} \nabla_{\theta} \pi(a \mid s) Q(s, a)+\pi(a \mid s) \sum_{s^{\prime}} p\left(s^{\prime} \mid s, a\right) \nabla_{\theta} V\left(s^{\prime}\right)
\end{equation}

\begin{equation}
\sum_{a} \nabla_{\theta} \pi(a \mid s) Q(s, a)+\sum_{a} \sum_{s^{\prime}} 
\pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \nabla_{\theta} V\left(s^{\prime}\right) 
\end{equation}

\begin{equation}
\phi(s)\leftarrow \sum_a \nabla_{\theta} \pi(a \mid s) Q(s, a)
\end{equation}

\begin{equation}
\left[\phi(s)\right] + 
\left [ \sum_{a} \sum_{s^{\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \nabla_{\theta} V\left(s^{\prime}\right)\right]
\end{equation}

\begin{equation}
\hspace*{-2cm} 
\left[  \phi(s)\right]+\left[\sum_{a} \sum_{s^{\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \phi\left(s^{\prime}\right)\right]+\left[\sum_{a} \sum_{s^{\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \sum_{a^{\prime}}\sum_{s^{\prime\prime}}\pi\left(a^{\prime} \mid s^{\prime}\right) p\left(s^{\prime\prime} \mid s^{\prime}, a^{\prime}\right) \nabla_{\theta} V\left(s^{\prime}\right) \right]
\end{equation}

\begin{equation}
\hspace*{-2cm} 
\left[ \phi(s)\right]+\left[\sum_{a} \sum_{s^{\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \phi\left(s^{\prime}\right)\right]+\left[\sum_{a} \sum_{s^{\prime}} \sum_{a^{\prime}}\sum_{s^{\prime\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \pi\left(a^{\prime} \mid s^{\prime}\right) p\left(s^{\prime\prime} \mid s^{\prime}, a^{\prime}\right) \nabla_{\theta} V\left(s^{\prime}\right) \right]
\end{equation}

% \begin{equation}
% \hspace*{-2cm} 
% \sum_{a} \phi(s)+\sum_{a} \sum_{s^{\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \phi\left(s^{\prime}\right)+\sum_{a} \sum_{s^{\prime}}\sum_{a^{\prime}}\sum_{s^{\prime\prime}}\pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \pi\left(a^{\prime} \mid s^{\prime}\right) p\left(s^{\prime\prime} \mid s^{\prime}, a^{\prime}\right) \nabla_{\theta} V\left(s^{\prime}\right)
% \end{equation}

\begin{equation}
\hspace*{-2.5cm} 
\left[ \phi(s)\right]+\left[\sum_{a} \sum_{s^{\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \phi\left(s^{\prime}\right)\right]+\left[\sum_{a} \sum_{s^{\prime}} \sum_{a^{\prime}}\sum_{s^{\prime\prime}} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right) \pi\left(a^{\prime} \mid s^{\prime}\right) p\left(s^{\prime\prime} \mid s^{\prime}, a^{\prime}\right) \phi\left(s^{\prime\prime}\right) \right] ...
\end{equation}

\begin{equation}
\rho\left(s \rightarrow s^{\prime}, 1\right) \leftarrow \sum_{a} \pi(a \mid s) p\left(s^{\prime} \mid s, a\right)
\end{equation}

\begin{equation}
\rho\left(s \rightarrow s^{\prime \prime}, 2\right)=\sum_{a} \sum_{s^{\prime}} \sum_{a^{\prime}} \pi (a \mid s) p\left(s^{\prime} \mid s, a\right) \pi\left(a^{\prime} \mid s^{\prime}\right) p\left(s^{\prime \prime} \mid s, a\right)
\end{equation}

\begin{equation}
\phi(s)+\sum_{a} \sum_{s^{\prime}} p\left(s\rightarrow s^{\prime}, 1\right) \phi\left(s^{\prime}\right)+\sum_{a} \sum_{s^{\prime}} \sum_{a^{\prime}} \sum_{s^{\prime \prime}} p\left(s \rightarrow s^{\prime \prime}, 2\right) \phi\left(s^{\prime \prime}\right) \ldots
\end{equation}

\begin{equation}
\nabla_{\theta}V(s) =  \sum_{k=0}^{\infty} \sum_{s} p(s \rightarrow s_k, k) \phi(s)
\end{equation}

\begin{equation}
    \nabla_{\theta} \text{J}(\theta)  = \nabla_{\theta}V(s_0)
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta)  = \nabla_{\theta}V(s_0) = \sum_{k=0}^{\infty} \sum_{s} p(s_0 \rightarrow s, k) \phi(s)
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta)  = \nabla_{\theta}V(s_0) = \sum_{s} \sum_{k=0}^{\infty} p(s \rightarrow s_k, k) \phi(s)
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) = \sum_{s} \eta (s) \phi(s)
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) = \sum_{s} \eta (s) \frac{\sum_{s} \eta (s)}{\sum_{s} \eta (s)} \phi(s)
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) = \left (\sum_{s} \eta (s) \right) \sum_{s} \frac{\eta (s)}{\sum_{s} \eta (s)} \phi(s)
\end{equation}

\begin{equation}
\mu(s) \leftarrow \frac{\eta (s)}{\sum_{s} \eta (s)}
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) = \left (\sum_{s} \eta (s) \right) \sum_{s} \mu(s)  \phi(s) \propto \sum_{s} \mu(s)  \phi(s) 
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) \propto \sum_{s} \mu(s) \sum_a \nabla_{\theta} \pi(a \mid s) Q(s, a)
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) \propto \mathrm{E}_{ \pi} \left [ \sum_a \nabla_{\theta} \pi(a \mid s) Q(s, a) \right]
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) \propto \mathrm{E}_{\pi} \left [ \sum_a \frac{\pi(a \mid s) }{\pi(a \mid s)} \nabla_{\theta} \pi(a \mid s)  Q(s, a) \right]
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) \propto \mathrm{E}_{\pi} \left [ \sum_a \frac{\nabla_{\theta} \pi(a \mid s)}{\pi(a \mid s)}  Q(s, a) \right]
\end{equation}

\begin{equation}
    \frac{\nabla_{\theta} \pi(a \mid s)}{\pi(a \mid s)}  = \log \nabla_{\theta} \pi(a \mid s)
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) \propto \mathrm{E}_{\pi} \left [ \sum_a \log \nabla_{\theta} \pi(a \mid s)  Q(s, a) \right]
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) \propto \mathrm{E}_{a \sim \pi} \left [ \log \nabla_{\theta} \pi(a \mid s)  Q(s, a) \right]
\end{equation}

\begin{equation}
    Q_{\pi} \left(s, a\right) = \mathrm{E}_{\pi}\left[R_{t} \mid s, a\right] = \mathrm{E}_{\pi}\left[\sum_{t^{\prime} = t}^{T-1} r_t | s_t, a_t\right] \approx \sum_{t^{\prime} = t}^{T-1} r_t \approx R_t
\end{equation}

\begin{equation}
\nabla_{\theta} \text{J}(\theta) \propto \mathrm{E}_{a \sim \pi} \left [ \log \nabla_{\theta} \pi(a \mid s) R_t \right]
\end{equation}
