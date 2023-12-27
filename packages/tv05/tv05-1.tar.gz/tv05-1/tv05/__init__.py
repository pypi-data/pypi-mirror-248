import pyperclip as pc
def n1():
    s = '''x = np.array(...)
std = 3.4
alpha = 0.01
m0 = 1.29
m1 = 1.17
n = len(x)
Z = n**0.5 * (x.mean() - m0) / std
za = norm(0, 1).isf(alpha / 2)
A = za
P = 2 * min(norm(0, 1).cdf(Z), norm(0, 1).sf(Z))
W = 2 - (norm(0, 1).cdf(za + n**0.5 * (m1 - m0) / std) + norm(0, 1).cdf(za - n**0.5 * (m1 - m0) / std))
Z, A, P, W
    '''
    return pc.copy(s)
    
def n2():
    s = '''x = np.array(...)
std = x.std(ddof = 1)
alpha = 0.05
m0 = 1.1
m1 = 0.91
n = len(x)
T = n**0.5 * (x.mean() - m0) / std
ta = t(n - 1).isf(alpha / 2)
A = ta
P = 2 * min(t(n - 1).cdf(T), t(n - 1).sf(T))
W = 1 - (nct(n - 1, n**0.5 * (m1 - m0) / std).cdf(ta) - nct(n - 1, n**0.5 * (m1 - m0) / std).cdf(-ta))
T, A, P, W
    '''
    return pc.copy(s)

def n3():
    s = '''x = np.array(...)
m = 1.18
alpha = 0.02
std = 1.14
std1 = 1.24
n = len(x)
X0 = sum((x - m)**2) / std**2
chia = chi2(n).isf(alpha / 2)
chi1_a = chi2(n).isf(1 - alpha / 2)
A = chi1_a
B = chia
P = 2 * min(chi2(n).cdf(X0), chi2(n).sf(X0))
b = chi2(n).cdf(std**2 / std1**2 * chia) - chi2(n).cdf(std**2 / std1**2 * chi1_a)
X0, A, B, P, b
    '''
    return pc.copy(s)
    
def n4():
    s = '''x = np.array(...)
alpha = 0.02
std = 1.14
std1 = 1.24
n = len(x)
X = (n - 1) * x.std(ddof = 1)**2 / std**2
chia = chi2(n - 1).isf(alpha / 2)
chi1_a = chi2(n - 1).isf(1 - alpha / 2)
A = chi1_a
B = chia
P = 2 * min(chi2(n - 1).cdf(X), chi2(n - 1).sf(X))
b = chi2(n - 1).cdf(std**2 / std1**2 * chia) - chi2(n - 1).cdf(std**2 / std1**2 * chi1_a)
X, A, B, P, b
    '''
    return pc.copy(s)
    
def n5():
    s = '''x = np.array(...)
y = np.array(...)
alpha = 0.02
std1 = 0.7
std2 = 1.4
n = len(x)
m = len(y)
mx_my = 0.1
Z = (x.mean() - y.mean()) / (std1**2 / n + std2**2 / m)**0.5
za = norm(0, 1).isf(alpha)
A = za
P = norm(0, 1).sf(Z)
W = 1 - norm(0, 1).cdf(za - (n * m)**0.5 / (m * std1**2 + n * std2**2)**0.5 * mx_my)
Z, P, A, W
    '''
    return pc.copy(s)

def n6():
    s = '''A = np.array(...)
B = np.array(...)
C = np.array(...)
ABC = np.concatenate([A, B, C])
alpha = 0.01
n = np.array([len(A), len(B), len(C)])
k = 3
N = len(ABC)
g = ABC.mean()
m = np.array([A.mean(), B.mean(), C.mean()])
var = np.array([A.var(), B.var(), C.var()])
d2 = sum((m - g)**2 * n) / N
std2_ = sum(var * n) / N
SSE = N * std2_
MSE = SSE / (N - k)
SSTR = N * d2
MSTR = SSTR / (k - 1)
F = MSTR / MSE
P = f(k - 1, N - k).sf(F)
d2, std2_, F, P
    '''
    return pc.copy(s)
    