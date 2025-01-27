import matplotlib.pyplot as plt
import pyfonts

# Load the font
pyfonts.load_font('Roboto')

# Set the font properties
plt.rcParams['font.family'] = 'Roboto'

# Create your plot
plt.plot([1, 2, 3, 4])
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot with Roboto Font')
plt.show()