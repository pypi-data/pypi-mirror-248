import pyperclip


def n0():
    s = r'''
n1 H0: mu = x, H1: mu != x через Z (дана сигма)
n1_1 все K и betta для n1
n2 H0: mu = x, H1: mu != x через T (ничего не дано)
n2_1 все K и betta для n2
n3 H0: si = x, H1: si != x через chi (дано mu)
n3_1 все K и betta для n3
n4 H0: si = x, H1: si != x через chi (ничего не дано)
n4_1 все K и betta для n4
n5 H0: mu_x = mu_y, H1: mu_x > mu_y через Z (var_x var_y известны)
n5_1 все K и betta для n5
n6 H0: mu_x = mu_y, H1: mu_x > mu_y через T (var_x var_y неизвестны но равны)
n6_1 все K и betta для n6
n7 H0: mu_x = mu_y, H1: mu_x != mu_y через df и T (var_x var_y неизвестны и не равны)
n8 H0: mu1 = mu2 = mu3 через F
n9 функция лапласа Phi
'''
    return pyperclip.copy(s)


def n1():
    s = r'''
x = np.array(значения)
n = len(x)

s = 3.4 #sigma
alpha = 0.01
mu0 = 1.29 #из гипотез
mu1 = 1.17 #из мощности

z = np.sqrt(n) * (x.mean() - mu0) / s
A = Z.isf(alpha / 2)
pv = 2 * min(Z.cdf(z), Z.sf(z))
beta = Phi0(A - np.sqrt(n) * (mu1 - mu0) / s) + Phi0(A + np.sqrt(n) * (mu1 - mu0) / s)
W = 1 - beta
z, A, pv, W '''
    return pyperclip.copy(s)


def n1_1():
    s = r'''
H1         K                  betta
mu > mu_0  z > z_alpha        1/2 + Phi0(z_alpha - sqrt(n) / s * (mu1 - mu0))
mu < mu_0  z < -z_alpha       1/2 + Phi0(z_alpha - sqrt(n) / s * (mu0 - mu1))
mu != mu_0 abs(z) z(alpha/2)  Phi0(A - sqrt(n) * (mu1 - mu0) / s) + Phi0(A + sqrt(n) * (mu1 - mu0) / s)
    '''
    return pyperclip.copy(s)


def n2_1():
    s = r'''
H1         K                        betta
mu > mu_0  t > t_alpha(n-1)         nct(n - 1, delta).cdf(t2)
mu < mu_0  t < -t_alpha(n-1)        1 - nct(n - 1, delta).cdf(-t2)
mu != mu_0 abs(t) > t(alpha/2, n-1) nct(n - 1, delta).cdf(t2) - nct(n - 1, delta).cdf(-t2)
    '''
    return pyperclip.copy(s)


def n2():
    s = r'''
x = np.array(значения)
n = len(x)

alpha = 0.05
mu0 = 1.1 #гипотеза
mu1 = 0.91 #мощность

T = np.sqrt(n) * (x.mean() - mu0) / x.std(ddof=1)
A = t(n - 1).isf(alpha / 2)
pv = 2 * min(t(n - 1).cdf(T), t(n - 1).sf(T))
delta = np.sqrt(n - 1) * (mu1 - mu0) / x.std()
t2 = t(n - 1).isf(alpha / 2)
beta = nct(n - 1, delta).cdf(t2) - nct(n - 1, delta).cdf(-t2)
W = 1 - beta
T, A, pv, W
'''
    return pyperclip.copy(s)


def n3():
    s = r'''
x = np.array(значения)
n = len(x)

alpha = 0.02
mu = 1.18 #дано
s0 = 1.14 #гипотеза
s1 = 1.24 #мощность

s2 = np.sum((x - mu) ** 2) / n

CHI = n * s2 / s0 ** 2

A = chi2(n).isf(1 - alpha / 2)
B = chi2(n).isf(alpha / 2)

pv = 2 * min(chi2(n).cdf(CHI), chi2(n).sf(CHI))

beta = chi2(n).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n).cdf(s0 ** 2 / s1 ** 2 * A)

CHI, A, B, pv, beta
'''
    return pyperclip.copy(s)


def n3_1():
    s = r'''
H1         K                              betta
si > si_0  от chi2(n, alpha) до +inf      chi2(n).cdf(s0 ** 2 / s1 ** 2 * chi2(n).isf(alpha)
si < si_0  от 0 до chi2(n, 1 - alpha)     1 - chi2(n).cdf(s0 ** 2 / s1 ** 2 * chi2(n).isf(1 - alpha)
si != si_0 оба интервала выше, но alpha/2 chi2(n).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n).cdf(s0 ** 2 / s1 ** 2 * A)
    '''
    return pyperclip.copy(s)


def n4():
    s = r'''
x = np.array(значения)
n = len(x)

alpha = 0.02 #дано
s0 = 1.14 #гипотеза
s1 = 1.24 #мощность
CHI = (n - 1) * x.var(ddof=1) / s0 ** 2
A = chi2(n - 1).isf(1 - alpha / 2)
B = chi2(n - 1).isf(alpha / 2)
pv = 2 * min(chi2(n - 1).cdf(CHI), chi2(n - 1).sf(CHI))
beta = chi2(n - 1).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n - 1).cdf(s0 ** 2 / s1 ** 2 * A)
CHI, A, B, pv, beta
    '''
    return pyperclip.copy(s)


def n4_1():
    s = r'''
H1         K                              betta
si > si_0  от chi2(n-1, alpha) до +inf    chi2(n-1).cdf(s0 ** 2 / s1 ** 2 * chi2(n-1).isf(alpha)
si < si_0  от 0 до chi2(n-1, 1 - alpha)   1 - chi2(n).cdf(s0 ** 2 / s1 ** 2 * chi2(n-1).isf(1 - alpha)
si != si_0 оба интервала выше, но alpha/2 chi2(n-1).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n-1).cdf(s0 ** 2 / s1 ** 2 * A)
    '''
    return pyperclip.copy(s)


def n5():
    s = r'''
x = np.array(значения x)
n = len(x)
y = np.array(значения y)
m = len(y)

sx = 0.7
sy = 1.4
alpha = 0.02
delta = 0.1

z = (x.mean() - y.mean()) / np.sqrt(sx ** 2 / n + sy ** 2 / m)
pv = Z.sf(z)
A = Z.isf(alpha)
beta = 1 / 2 + Phi0(A - np.sqrt(m * n) / np.sqrt(m * sx ** 2 + n * sy ** 2) * delta)
W = 1 - beta
z, pv, A, W
    '''
    return pyperclip.copy(s)


def n5_1():
    s = r'''
H1           K                    betta
mu_x > mu_y  z > z_alpha          1 / 2 + Phi0(z_alpha - np.sqrt(m * n) / np.sqrt(m * sx ** 2 + n * sy ** 2) * delta)
mu_x < mu_y  z < -z_alpha         1 / 2 + Phi0(z_alpha + np.sqrt(m * n) / np.sqrt(m * sx ** 2 + n * sy ** 2) * delta)
mu_x != mu_y abs(z) > z_(alpha/2) сумма 1 и 2, но без 1/2, только части с фи
    '''
    return pyperclip.copy(s)


def n6():
    s = r'''
X = данные
Y = данные
n = len(X)
m = len(Y)

sx = X.std(ddof=1)
sy = Y.std(ddof=1)
alpha = 0.04

sp2 = (n - 1) / (n + m - 2) * sx ** 2 + (m - 1) / (n + m - 2) * sy ** 2
sp = np.sqrt(sp2)

T = (X.mean() - Y.mean()) / (sp * np.sqrt(1/n + 1/m))

abs(T) > t.isf(alpha/2, n + m - 2)
pv = 2 * min(t(n + m - 2).cdf(T), t(n + m - 2).sf(T))
    '''
    return pyperclip.copy(s)


def n6_1():
    s = r'''
H1           K                          betta
mu_x > mu_y  t > t(n+m-2, alpha)        нет
mu_x < mu_y  t < -t(n+m-2, alpha)       нет
mu_x != mu_y abs(t) > t(n+m-2, alpha/2) нет
    '''
    return pyperclip.copy(s)


def n7():
    s = r'''
X = данные
Y = данные
n = len(X)
m = len(Y)

alpha = 0.05
sx = X.std(ddof=1)
sy = Y.std(ddof=1)

sw = np.sqrt(sx ** 2 / n + sy ** 2 / m)
t_w = (X.mean() - Y.mean()) / sw
theta = X.var(ddof=1) / Y.var(ddof=1)
df = (theta + n/m)**2 / (1/(n - 1) * theta **2 + 1/(m-1) * (n/m)**2)
abs(t_w) > t.isf(alpha/2, df) #входит ли в K
pv = 2 * min(t(df).cdf(t_w), t(df).sf(t_w))
    '''
    return pyperclip.copy(s)


def n8():
    s = r'''
x = np.array(данные)
n1 = len(x)

y = np.array(данные)
n2 = len(y)

z = np.array(данные)
n3 = len(z)

xyz = pd.DataFrame([x, y, z]).T
xyz_all = np.concatenate([x, y, z])
n = [n1, n2, n3]
N = sum(n)
k = 3
alpha = 0.01

d2 = np.sum((xyz.mean() - xyz_all.mean()) ** 2 * n) / N
meanvar = np.sum(xyz.var(ddof=0) * n) / N

(d2 + meanvar), xyz_all.var(ddof=0) # проверка

SSE = N * meanvar
MSE = SSE / (N - k)
SSTR = N * d2
MSTR = SSTR / (k - 1)
F = MSTR / MSE
pv = f(k - 1, N - k).sf(F)

d2, meanvar, F, pv
    '''
    return pyperclip.copy(s)


def n9():
    s = r'''
Z = norm()

def Phi0(x):
    return Z.cdf(x) - 1 / 2 '''
    return pyperclip.copy(s)
