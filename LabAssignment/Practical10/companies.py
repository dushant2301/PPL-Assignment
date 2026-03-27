import pandas as pd
import matplotlib.pyplot as plt

# 1. Create/Import Dataset
data = {
    'Company': ['Microsoft', 'Google', 'Amazon', 'IBM', 'Deloitte', 'Capgemini', 'ATOS Origin', 'Amdocs'],
    'Recruitments': [450, 600, 550, 300, 400, 350, 200, 250]
}
df = pd.DataFrame(data)

# a) Bar Chart
plt.figure(figsize=(10, 5))
plt.bar(df['Company'], df['Recruitments'], color='skyblue', edgecolor='black')
plt.title('New Recruitments by Company (Bar Chart)')
plt.xlabel('Company')
plt.ylabel('Number of Recruitments')
plt.show()

# b) Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(df['Recruitments'], labels=df['Company'], autopct='%1.1f%%')
plt.title('Distribution of New Recruitments')
plt.show()

# c) Customize Pie Chart (Exploding, Shadow, and Colors)
explode = [0.1 if x == 'Google' else 0 for x in df['Company']] # Highlight Google
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#c4e17f','#76D7C4']

plt.figure(figsize=(8, 8))
plt.pie(df['Recruitments'], labels=df['Company'], autopct='%1.1f%%', 
        startangle=140, explode=explode, shadow=True, colors=colors)
plt.title('Customized Recruitment Distribution')
plt.show()

# d) Doughnut Chart
plt.figure(figsize=(8, 8))
plt.pie(df['Recruitments'], labels=df['Company'], autopct='%1.1f%%', startangle=140, colors=colors)
# Draw a white circle at the center to make it a doughnut
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('New Recruitments (Doughnut Chart)')
plt.show()

# e) Compare IBM & Amdocs
comparison_df = df[df['Company'].isin(['IBM', 'Amdocs'])]
plt.figure(figsize=(6, 5))
plt.bar(comparison_df['Company'], comparison_df['Recruitments'], color=['orange', 'green'])
plt.title('Comparison: IBM vs Amdocs Recruitments')
plt.ylabel('Recruitments')
plt.show()