import numpy as np
import matplotlib.pyplot as plt
import datetime
import platform

class MultiOpt:
    def __init__(self, X, scores):
        """
        ================================================================
        PACKAGE: The Tool Kit of Bgolearn package .
        Author: Bin CAO <binjacobcao@gmail.com> 
        Guangzhou Municipal Key Laboratory of Materials Informatics, Advanced Materials Thrust,
        Hong Kong University of Science and Technology (Guangzhou), Guangzhou 511400, Guangdong, China
        ================================================================
        Please feel free to open issues in the Github :
        https://github.com/Bin-Cao/Bgolearn
        or 
        contact Mr.Bin Cao (bcao686@connect.hkust-gz.edu.cn)
        in case of any problems/comments/suggestions in using the code. 
        ==================================================================
        Thank you for choosing Bgolearn for material design. 
        Bgolearn is developed to facilitate the application of machine learning in research.

        Bgolearn is designed for optimizing single-target material properties. 
        The BgoKit package is being developed to facilitate multi-task design.
        ================================================================
        :param X: virtual samples, X .

        :param scores: scores = [score_1,score_2], the scores of different targets

        example:
        from BgoKit import ToolKit
        # X is the virtual samples
        # score_1, score_2 are output of Bgolearn
        # score_1, _= Mymodel_1.EI() ; score_2, _= Mymodel_2.EI()

        Model = ToolKit.MultiOpt(X,[score_1,score_2])
        Model.BiSearch()
        Model.plot_distribution()
        """
        self.X = np.array(X)
        self.scores = scores
        self.font = {'family' : 'Arial',
                'weight' : 'normal',
                'size'   : 23,
                }
        
        now = datetime.datetime.now()
        self.time = now.strftime('%Y-%m-%d %H:%M:%S')

    def BiSearch(self):
        if len(self.scores) == 2: pass
        else: 
            print('Search_bi is implemented for only two design targets')
            raise ValueError
        Tone = (self.scores[0] - self.scores[0].min()) / (self.scores[0].max()-self.scores[0].min())
        Ttwo = (self.scores[1] - self.scores[1].min()) / (self.scores[1].max()-self.scores[1].min())

        pareto_front = find_pareto_front(Tone,Ttwo)
        sums = pareto_front[:,0] + pareto_front[:,1]
        opt_index = np.argmax(sums)
        val_one = pareto_front[:,0][opt_index]
        val_two = pareto_front[:,1][opt_index]
        indices = np.where((pareto_front[:,0] == val_one) & (pareto_front[:,1] == val_two))[0]
        print(indices)
        xx = np.arange(5,95)/100
        
        fig = plt.figure(figsize=[8,8])
        plt.scatter(Tone, Ttwo, marker='o', edgecolor='gray',label='virtual samples')
        plt.scatter(pareto_front[:,0],pareto_front[:,1], marker='o', c='cyan', edgecolor='k',label='Pareto front')
        plt.scatter(val_one,val_two ,marker='*', c='red', s=150, edgecolor='k',label='candidates')
        plt.plot(xx, val_one+val_two-1*xx,c='y',linestyle='--',alpha=0.6,)
        plt.xlabel('utility values of Object one ',self.font)
        plt.ylabel('utility values of Object two',self.font)
        plt.xlim(-0.05, 1.05)  
        plt.ylim(-0.05, 1.05) 
        plt.legend(fontsize=13,)
        plt.tick_params(labelsize=20)
        plt.legend(fontsize=13,loc=1)
        plt.savefig('ParetoF.png', dpi=800)
        plt.savefig('ParetoF.svg', dpi=800)
        plt.show()

        print('The optimal condidate recommended by BgoKit is :', self.X[indices])
        return self.X[indices]

    def plot_distribution(self):
        plt.figure(figsize=(10, 6))
        for i, task_scores in enumerate(self.scores):
            task_scores = (task_scores - task_scores.min()) / (task_scores.max()-task_scores.min())
            plt.subplot(1, 2, i + 1)
            plt.hist(task_scores, bins=20, alpha=0.7, color='skyblue')
            plt.title(f'Distribution of Score {i + 1}')
            plt.xlabel(f'Score{i + 1}')
            plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig('distribution.png', dpi=800)
        plt.savefig('distribution.svg', dpi=800)
        plt.show()
        


def is_pareto_efficient(costs):
    """
    Check if a solution is Pareto efficient.
    """
    num_solutions = costs.shape[0]
    is_efficient = np.ones(num_solutions, dtype=bool)

    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] >= c, axis=1)
            is_efficient[i] = True  # Current solution is always part of the Pareto front

    return is_efficient

def find_pareto_front(x_values, y_values):
    """
    Find points belonging to the Pareto front.
    """
    performance_array = np.column_stack((x_values, y_values))
    pareto_front = performance_array[is_pareto_efficient(performance_array)]
    
    return pareto_front
