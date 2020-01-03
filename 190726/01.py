#列表
list_a=["我自横刀向天笑"]
list_b=["去留肝胆两昆仑"]
'''
print(list_a+list_b)
print(list_a,list_b)
print(list_a,'\n',list_b)
list_a.append(list_b)
print(list_a)
list_a.extend(list_a[1:5])
print(list_a)
'''

print(list_a)
print(list_b)
str3=[]
str3.extend(list_a)
str3.extend(list_b)
print(str3)
print(str3[0])
print(str3[1])

str4='山不在高有仙则名'
str5='水不在深有龙则名'
print(str4,str5)
print(str4,'\n',str5,sep='')

str6=['我自横刀向天笑','去留肝胆两昆仑','山不在高有仙则名','水不在深有龙则名']
print('str6=:',str6,type(str6),sep='\n')

print(str6[0],str6[1],str6[2],str6[3],sep=' ')
print(str6[0]+str6[1]+str6[2]+str6[3])
print(list_a+list_b,str4+str5)

str3.remove('山不在高有仙则名') if '山不在高有仙则名' in str3 else (str3.remove('去留肝胆两昆仑') if '去留肝胆两昆仑' in str3 else str3.clear())
print('now:',str3)

print('--------------------------------------------------------------------')
list_1=[list_a,list_b,str4,str5]
print(list_1)
print(list_1==str6)
print(type(list_1),type(list_1[0]),type(list_1[2]))
print(type(list_1))
print(type(list_1[0]))
print(type(list_1[2]))

print('--------------------------------------------------------------------')
del list_1[0]
print(list_1)
del list_1[0]
print(list_1)
del list_1[0]
print(list_1)
del list_1[0]
print(list_1)

print('--------------------------------------------------------------------')
list_1=[list_a,list_b,str4,str5]

list_1[0]=None
print(list_1[0])
list_1[1]=None
print(list_1)
list_1[2]='\t'
print(list_1)
list_1[3]='\b'
print(list_1)

print(list_1[0])
print(list_1[1])
print(list_1[2])
print(list_1[3])

print('--------------------------------------------------------------------')
list_1=[list_a,list_b,str4,str5]
print(list_1)
del list_1[1]
list_1[1:1]=[list_b]
print(list_1)
del list_1[2:]
print(list_1)
list_1[2:]=[[str4],[str5]]
print(list_1)

print('--------------------------------------------------------------------')
list_1=[list_a,list_b,str4,str5]
print(list_1)
print('%s'%list_1[0][0][2])

list_1[0]=list_a[0]
list_1[1]=list_b[0]
list_1[2]=str4
list_1[3]=str5
print(list_1)
print(list_1[0][2])

print('--------------------------------------------------------------------')
list_1[0:]=list_1[0]
print(type(list_1[0]+list_1[1]+list_1[2]+list_1[3]+list_1[4]+list_1[5]+list_1[6]))
print(type(list_1))
list_1.reverse()
print((list_1[0]+list_1[1]+list_1[2]+list_1[3]+list_1[4]+list_1[5]+list_1[6]))
list_1.sort()
print((list_1[0]+list_1[1]+list_1[2]+list_1[3]+list_1[4]+list_1[5]+list_1[6]))