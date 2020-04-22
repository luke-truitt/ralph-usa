from algDev.algorithms.asset_allocation import AssetAllocation

class AssetStrategy:

    def __init__(self, asset_allocation, close_type='threshold'):
        self.asset_allocation = asset_allocation

        self.close_types = 
        assert close_type in self.algorithm_types = ['threshold', 'daily']
        self.close_type = close_type

    def allocate(self, date, positions, predictions, verbose=False):
        return self.asset_allocation.calculate_allocations( date, positions, predictions, verbose)