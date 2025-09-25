from matplotlib import pyplot as plt # Mudança de 'pyplot' para 'plt' para padrão
import numpy as np # Adicionado numpy

class DrawNN():
    def __init__(self, neural_network, weights_list=None, orientation='vertical'):
        self.neural_network = neural_network
        self.weights_list = weights_list
        self.orientation = orientation

    def draw(self):
        # Configurações de desenho
        if self.orientation == 'vertical':
            # Para orientação vertical, camadas empilhadas verticalmente
            layer_spacing_x = 2
            neuron_spacing_y = 1
            neuron_radius = 0.5
            figsize_ratio = (1.5 * max(self.neural_network), 1.0 * len(self.neural_network)) # Mais largo que alto
        else: # Horizontal (comportamento original, apenas como referência)
            layer_spacing_x = 6
            neuron_spacing_y = 2
            neuron_radius = 0.5
            figsize_ratio = (2.5 * len(self.neural_network), 2.5 * max(self.neural_network)) # Mais alto que largo

        number_of_layers = len(self.neural_network)
        max_number_of_neurons = max(self.neural_network)
        
        # Ajusta o y_top ou x_left inicial para centralizar
        if self.orientation == 'vertical':
            start_x = (max_number_of_neurons - 1) * neuron_spacing_y / 2 # Centro horizontal
            fig = plt.figure(figsize=figsize_ratio)
            ax = fig.gca()
            ax.axis('off')

            layer_center_x = []
            for layer_size in self.neural_network:
                layer_center_x.append((layer_size - 1) * neuron_spacing_y / 2) # Centro de cada camada
            
            y_pos = 0 # Posição Y inicial para a primeira camada (topo)
            for i in range(number_of_layers):
                x_layer_neurons = [(start_x - layer_center_x[i]) + (j * neuron_spacing_y) for j in range(self.neural_network[i])]
                
                for j in range(self.neural_network[i]):
                    circle = plt.Circle((x_layer_neurons[j], y_pos), neuron_radius, color='w', ec='k', zorder=4)
                    ax.add_artist(circle)
                    
                # Avança para a próxima camada abaixo
                y_pos -= layer_spacing_x 
            
            # Desenhar as conexões
            y_pos_start = 0
            for i in range(number_of_layers - 1):
                y_pos_next = y_pos_start - layer_spacing_x
                
                # Coordenadas X para neurônios da camada atual
                x_layer_neurons_current = [(start_x - layer_center_x[i]) + (j * neuron_spacing_y) for j in range(self.neural_network[i])]
                # Coordenadas X para neurônios da próxima camada
                x_layer_neurons_next = [(start_x - layer_center_x[i+1]) + (j * neuron_spacing_y) for j in range(self.neural_network[i+1])]

                for j in range(self.neural_network[i]):
                    for k in range(self.neural_network[i + 1]):
                        ax.plot([x_layer_neurons_current[j], x_layer_neurons_next[k]],
                                [y_pos_start, y_pos_next],
                                'k-', zorder=1)
                y_pos_start = y_pos_next 
                
        else:

            y_top = (max_number_of_neurons - 1) * neuron_spacing_y / 2
            fig = plt.figure(figsize=figsize_ratio)
            ax = fig.gca()
            ax.axis('off')

            layer_top_y = []
            for layer_size in self.neural_network:
                layer_top_y.append((layer_size - 1) * neuron_spacing_y / 2)

            left = 0
            for i in range(number_of_layers):
                layer_y = [(y_top - layer_top_y[i]) + (j * neuron_spacing_y) for j in range(self.neural_network[i])]
                
                for j in range(self.neural_network[i]):
                    circle = plt.Circle((left, layer_y[j]), neuron_radius, color='w', ec='k', zorder=4)
                    ax.add_artist(circle)
                    
                left += layer_spacing_x

            for i in range(number_of_layers - 1):
                for j in range(self.neural_network[i]):
                    for k in range(self.neural_network[i + 1]):
                        ax.plot([i * layer_spacing_x, (i + 1) * layer_spacing_x],
                                [(y_top - layer_top_y[i]) + (j * neuron_spacing_y), (y_top - layer_top_y[i + 1]) + (k * neuron_spacing_y)],
                                'k-', zorder=1)

        ax.set_aspect('equal', adjustable='box')
        plt.tight_layout()