import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)


plt.rcdefaults()
fig, ax = plt.subplots()

# Example data
programas = ('asistencia social', 'Empleo', 'Sanidad', 'Educacion', 'Deporte', 'Cultura', 'transporte publico', 'Deuda publica','seguridad y movilidad ciudadana', 'Viviendas y urbanismo','Bienestar comunitario','Medio Ambiente')
y_pos = np.arange(len(programas))

inversion =[79914837.63,13848619.44,6584352.60,41944159.90,57998052.77,17524346.28,48064522.75,76449915.00,
142484523.82,41188206.58,114371592.95,36182655.35]

total =811397108

porcentaje = []

for valor in inversion:
   porcentaje.append((valor/total)*100)

#performance = 3 + 10 * np.random.rand(len(people))
#error = np.random.rand(len(people))
#print(error)
i = 0
j = 0
#color = ['green','blue', 'orange', 'yellow', 'cyan', 'purple', 'pink','red','brown']
color = [(0.48,0.25,0.08), (0.34, 0.28, 0.24),(1,0.13,0),(64/255,1,111/255),(28/255,204/255,20/255),(122/255,176/255,20/255),(1,229/255,0),
         (64/255,74/255,1),(20/255,79/255,204/255),(61/255,70/255,88/255),(0,216/255,1),(1,0.5,64/255)]
#color = ['CC4A14','4C583D']

factores = ["79.9M","138.5M","6.5M","41.9M","57.9M","17.5M","48.0M","76.4M","14.2M","41.2M","114.4M","36.2M"]

for valor in porcentaje:
   ax.barh(factores[i], valor,  align='center',
        color=color[j], ecolor='black')
   i+=1
   j+=1
   if j == len(inversion):
      j = 0

porcentaje = int(max(porcentaje) + 1)
porcentaje = np.linspace(0,porcentaje,5)

ax.set_yticks(y_pos)
ax.set_xticks(porcentaje)
#ax.set_yticklabels(programas)
ax.invert_yaxis()  # labels read top-to-bottom
ax.legend(programas)
ax.set_xlabel('porcentaje')
ax.set_title('How fast do you want to go today?')

plt.show()
