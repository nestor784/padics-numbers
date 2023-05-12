class NumberP:
    p = 7
    def __init__(self,q):
        if '.' in q:
            if len([u for u in q.split('.')[0] if u!='0']) == 0 and  len([u for u in q.split('.')[1] if u!= '0']) == 0:
                self.q = '0.0'
            else:
                q = q.replace('0',' ').strip().replace(' ','0')
                if q.split('.')[1] == '':
                    q = q.split('.')[0]+'.0'
                self.q = q
        else:
            if len([u for u in q if u != '0'])==0:
                self.q = '0.0'
            else:
                self.q = q.replace('0',' ').lstrip().replace(' ','0') + '.0'
    def __str__(self):
        return '...'+self.q

    @property
    def norm(self):
        return self.p ** -self.order
    
    @property
    def len(self):
        return len(self.q)
    @property
    def show(self):
        return self.q

    @property
    def order(self):
        q = self.q.split('.')
        if q[1] != '0':
            return -len(q[1])
        else:
            t = [0 if i=='0' else 1 for i in q[0][::-1]]
            return t.index(1)
        
    def __add__(self,v1):
        u = self.show.split('.')
        v = v1.show.split('.')
        N = max(len(u[0]),len(v[0]))
        n = max(len(u[1]),len(v[1]))
        u = u[0].rjust(N,'0') + '.' + u[1].ljust(n,'0')
        v = v[0].rjust(N,'0') + '.' + v[1].ljust(n,'0')
        e = 0
        c = ''
        for s,t in zip(u[::-1],v[::-1]):
            if s == '.':
                c += '.'
            else:
                if int(s) + int(t) + e < self.p:
                    c += str(int(s) + int(t) + e)
                    e = 0
                else:
                    c += str(int(s) + int(t) + e-self.p)
                    e = 1
        c += str(e)
        return NumberP(c[::-1])


    def __sub__(self,v1):
        c = ''
        i = True
        for s in v1.show[::-1]:
            if s == '.':
                c+= '.'
            else:    
                if i:
                    if s == '0':
                        c += '0'
                    else:
                        c += str(self.p - int(s))
                        i = False
                else:
                    c += str(self.p - 1 - int(s))
        c += str(self.p - 1)*6
        c = NumberP(c[::-1])
        return self.__add__(c)

    def __mul__(self,v1):
        if self.show == '0.0' or v1.show == '0.0':
            return NumberP('0')

        u, n = self.asunit
        v, k = v1.asunit
        sum_of_expansion_v = [self.deltaproduct(u,(int(s),i)) for i,s in enumerate(v.show.split('.')[0][::-1])]
        result = NumberP('0.0')
        for u in sum_of_expansion_v:
            result += u
        if k+n != 0:
            if k+n > 0:
                r = result.show[::-1][2:]
                result = (r[:k+n] + '.' + r[k+n:])[::-1]
                return NumberP(result)
            else:
                r = result.show[::-1][2:]
                r += '0'*(-(k+n))
                return NumberP(r)
        return result

    @property
    def asunit(self):
        u = self.show
        if u != '0.0':
            uu = u.split('.')
            if uu[1] == '0':
                ubuffer = uu[0][::-1]
                if ubuffer[0] == '0':
                    return NumberP(ubuffer[self.order:][::-1]), -self.order
                else:
                    return NumberP(ubuffer[::-1]), 0
            else:
                return NumberP(u.replace('.','')), len(uu[1])
        else:
            return NumberP('0.0'), 0

    def deltaproduct(self,u,r):
        c = ''
        e = 0
        for s in u.show.split('.')[0][::-1]:
            if int(s)*r[0] + e < self.p:
                c += str(int(s)*r[0]+e)
                e = 0
            else:
                buffer = (int(s)*r[0]+e) % self.p
                c += str(buffer)
                e = (int(s)*r[0]+e-buffer) // self.p
        c += str(e)
        return NumberP(c[::-1].ljust(len(c)+r[1],'0').replace(' ','0'))


    def __truediv__(self,v1):
        if v1.show == '0.0':
            return 'Zero Division Error'
        u, n = self.asunit
        v, k = v1.asunit
        c = ''
        d = 'w'
        w=1
        dividendo = NumberP(u.show)
        while w<15:
            c+= d
            t = [(i, v*NumberP(str(i))) for i in range(self.p)]
            r = [u[0] for u in t if u[1].show.split('.')[0][-1] == dividendo.show.split('.')[0][-1]]
            iadic = NumberP(str(max(r)))
            d = str(max(r))
            index = self.auxiliar(dividendo,v*iadic) 
            c+= '0'*index
            dividendo = self.deltasustraction(dividendo, v*iadic)
            w+=1
        c = c.replace('w','')
        return NumberP(c[::-1])

    def deltasustraction(self,u,v):
        s = u.show.split('.')[0]
        t = v.show.split('.')[0]
        N = max(len(s),len(t))
        s = s[::-1].ljust(N,'0')
        t = t[::-1].ljust(N,'0')
        c = ''
        e = 0
        for j in range(N): 
            buff = int(s[j])-int(t[j])-e
            if buff < 0:
                e = 1
            else:
                e = 0
            c += str(buff % self.p)
        if e == 1:
            c += str(self.p - 1)
        if s[N-1] == '0':
            c = c.ljust(20,str(self.p -1))
        r, _ = NumberP(c[::-1]).asunit
        return r

    @staticmethod
    def auxiliar(u,v):
        s = u.show.split('.')[0][::-1]
        t = v.show.split('.')[0][::-1]
        for i in range(min(len(s),len(t))):
            if s[i] != t[i] and i > 0:
                return i-1
        return 0

if __name__ == "__main__":
    x = NumberP('200.01')
    y = NumberP('100')
    z = NumberP('0')
    print(x*y)
