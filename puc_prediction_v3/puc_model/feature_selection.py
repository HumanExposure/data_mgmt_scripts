#Feature selection adapted from:
##https://towardsdatascience.com/designing-a-feature-selection-pipeline-in-python-859fec4d1b12
import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import KFold
from sklearn.feature_selection import RFECV
from boruta import BorutaPy
from sklearn.feature_selection import SelectPercentile, chi2
from scipy import stats
import math

class FeatureSelector:
    """
    The FeatureSelector class implement the following feature selection 
    methods:
        
    
    1. A method that removes features with very similar values. For example,
    a feature that contains 0 for every instance.
    
    2. A filter method that removes correlated features based on Pearson or
    Spearman's coefficient.
    
    3. A recursive feature elimination algorithm with cross validation.
    
    4. The Boruta method which uncovers features that are relevant to
    the outcome.
    
    
    Parameters
    ----------
    
    None
        
    Example
    -------
    
    # Define steps
    step1 = {'Constant Features': {'frac_constant_values': 0.90}}
    
    step2 = {'Correlated Features': {'correlation_threshold': 0.95}}
    
    step3 = {'Relevant Features': {'estimator': estimator,
                                   'cv': 5,
                                    'n_estimators': 1000,
                                    'max_iter': 100,
                                    'verbose': 50,
                                    'random_state': 42}}
    
    step4 = {'RFECV Features': {'estimator': estimator,
                                'cv': 2,
                                'step': 1,
                                'scoring': 'accuracy',
                                'verbose': 50,}}
    
    # Place steps in a list in the order you want them execute it
    steps = [step1, step2, step3, step4]
    
    # Initialize FeatureSelector()
    fs = FeatureSelector()
    
    # Apply feature selection methods
    X_selected = fs.fit(X_all_train, y_all_train, steps)
    
    
    Attributes
    ----------
    
    
    Author Information
    ------------------
    Frank Ceballos
    LinkedIn: <https://www.linkedin.com/in/frank-ceballos/>
    Date: January 31, 2020
    """
    
    
    def __init__(self):
        self.rfecv = None
        self.selected_features = None
    
    
    def fit(self, X, y, steps = {}):
        """
        Calls the feature selection methods in the order specified in steps and
        determines the selected features. 
        
        
        Parameters
        ----------
        X : pandas dataframe
            A data set where each row is an observation and each column a feature.
        
        y: numpy array
            A numpy array containing the targets
            
        steps: list
            The list of steps that determines the order to apply the
            feature selection algorithms. Each element in this list is a dict,
            where key can be:
                            'Constant Features', 
                            'Correlated Features'
                            'Relevant Features'
                            'RFECV Features'
            and the value is a dict with the parameters used to execute 
            the feature selection method.
            
            
        Returns
        -------
        None
        """
        
        # Determine if there are any methods that are not defined
        for step in steps:
            available_methods = ['Constant Features', 'Correlated Features', 
                                 'Relevant Features', 'RFECV Features',
                                 'ANOVA Features']
            
            for key, value in step.items():
                if key not in available_methods:
                    print(f'{key} is not a valid key!')
                    print(f'Only these are available: {available_methods}')
                    print(f'Redefine the key in this dict/step: {step}')
                    print('Now exiting function!')
                    return None
        
        # Get the order the methods are going to be applied
        method_order = [[*step][0] for step in steps]
        
        # Get methods
        ordered_methods = self.get_methods(method_order)
        
        # Initiate empty list of labels to drop
        drop_features = []
        
        # Temporary features
        X_temp = X.copy()
        
        if isinstance(X_temp, np.ndarray): #If array, keep track of columns removed/selected
            #print('np.ndarrays not supported at this time...returning')    
            #return None
            print('Storing array column dictionary')
            self.array_dict = {'selected':[str(n) for n in range(X.shape[1])],
                               'to_select':[str(n) for n in range(X.shape[1])]
                               }
        else:
            self.array_dict = None
        
        for method_label in method_order:
            
            # Get method
            method = ordered_methods[method_label]
            
            # Get method parameters
            for step in steps:
                if method_label in step.keys():
                    params = step[method_label]
            
            
            # Determine features to drop
            if method_label in ['Constant Features', 'Correlated Features']:
                 # Message to user
                print(f'Removing {method_label}' + ' ----- ' + str(datetime.datetime.now()))
                if X_temp.shape[1] == 1:
                    print('Only 1 feature to select against...returning')
                    continue
                drop_features_temp = method(X_temp, self.array_dict, **params)
                print(f'Features removed: {len(drop_features_temp)}')
                #print(drop_features_temp)
                print('')
                                
                # Update feature matrix
                if isinstance(X_temp, np.ndarray): #Handle Array
                    # Append features to drop list
                    #HANDLE THE MAPPING TO INDEX CHANGES USING ARRAY DICTIONARY
                    drop_features = drop_features + [self.array_dict['selected'][i] for i in drop_features_temp]
                    if len(drop_features) == 0:
                       print(f'{method_label} didn\'t remove any features...')
                       continue
                    elif len(drop_features) == len(self.array_dict['selected']):
                        print("Step removed all features...reverting selection...")
                    else:
                        #Update selected features list
                        self.array_dict['selected'] = [self.array_dict['selected'].remove(x) for x in drop_features]
                        #Reset X_temp to selected columns
                        X_temp = X.copy()
                        X_temp = X_temp[:, [int(i) for i in self.array_dict['selected']]]
                        #Reset to_select index
                        self.array_dict['to_select'] = [str(n) for n in range(X_temp.shape[1])]
                else: #Handle Dataframe
                    # Append features to drop list
                    drop_features = drop_features + drop_features_temp
                    if len(drop_features) == len(X_temp.columns):
                        print("Step removed all features...reverting selection...")
                    else:
                        X_temp = X.drop(columns = drop_features, axis = 1)
                        
            elif method_label in ['Relevant Features']:                    
                print('Selecting relevant features' + ' ----- ' + str(datetime.datetime.now()))
                print("Boruta method not tested for np.ndarray! Skipping...")
                continue
                if X_temp.shape[1] == 1:
                    print('Only 1 feature to select against...returning')
                    continue
                relevant_features_temp = method(X_temp, self.array_dict, y, params)
                print(f'Features selected: {len(relevant_features_temp)}')
                print('Finished selecting relevant features' + ' ----- ' + str(datetime.datetime.now()))
                #print(relevant_features_temp)
                print('')
                
                # Update feature matrix
                if len(relevant_features_temp) == 0:
                    print("Step removed all features...reverting...")
                else:
                    if isinstance(X_temp, np.ndarray): #From array
                        print("Boruta method not tested for np.ndarray! Check results...")    
                        self.array_dict['selected'] = [self.array_dict['selected'][int(i)] for i in relevant_features_temp]
                        #Reset X_temp to selected columns
                        X_temp = X.copy()
                        X_temp = X_temp[:, [int(i) for i in self.array_dict['selected']]]
                        #Reset to_select index
                        self.array_dict['to_select'] = [str(n) for n in range(X_temp.shape[1])]    
                    else: #From data frame
                        X_temp = X[relevant_features_temp]
            
            
            elif method_label in ['RFECV Features']:
                print('Selecting RFECV features' + ' ----- ' + str(datetime.datetime.now()))
                if X_temp.shape[1] == 1:
                    print('Only 1 feature to select against...returning')
                    continue
                rfecv_features_temp, feature_selector = method(X_temp, y, self.array_dict, params)
                print(f'Features selected: {len(rfecv_features_temp)}')
                #print(rfecv_features_temp)
                print('')
                
                # Save fitted rfecv 
                self.rfecv = feature_selector
                
                # Update feature matrix
                if len(rfecv_features_temp) == 0:
                    print("Step removed all features...reverting...")
                else:
                    if isinstance(X_temp, np.ndarray): #From array
                        self.array_dict['selected'] = [self.array_dict['selected'][int(i)] for i in rfecv_features_temp]
                        #Reset X_temp to selected columns
                        X_temp = X.copy()
                        X_temp = X_temp[:, [int(i) for i in self.array_dict['selected']]]
                        #Reset to_select index
                        self.array_dict['to_select'] = [str(n) for n in range(X_temp.shape[1])]    
                    else: #From data frame
                        X_temp = X[rfecv_features_temp]
            elif method_label in ['ANOVA Features']:
                print('Selecting ANOVA features' + ' ----- ' + str(datetime.datetime.now()))
                if X_temp.shape[1] == 1:
                    print('Only 1 feature to select against...returning')
                    continue
                anova_features_temp = method(X_temp, y, self.array_dict, params)
                print(f'Features selected: {len(anova_features_temp)}')
                print('')
                #print(anova_features_temp)
                # Update feature matrix
                if len(anova_features_temp) == 0:
                    print("Step removed all features...reverting...")
                else:
                    if isinstance(X_temp, np.ndarray): #From array
                        self.array_dict['selected'] = [self.array_dict['selected'][int(i)] for i in anova_features_temp]
                        #Reset X_temp to selected columns
                        X_temp = X.copy()
                        X_temp = X_temp[:, [int(i) for i in self.array_dict['selected']]]
                        #Reset to_select index
                        self.array_dict['to_select'] = [str(n) for n in range(X_temp.shape[1])]    
                    else: #From data frame
                        X_temp = X[anova_features_temp]
                
        # Save selected features
        if isinstance(X_temp, np.ndarray): #From array
            self.selected_features = [int(i) for i in self.array_dict['selected']]
        else: #From dataframe
            self.selected_features = list(X_temp.columns)
        
        # Message to user
        message = 'Done selecting features'
        
        return(print(message))
    
    def transform(self, X):
        """
        Returns a dataframe with the selected features determine with fit()
        
        
        Parameters
        ----------
        X : pandas dataframe
            A data set where ech row is an observation and each column a feature.
        
        Returns
        -------
        X_selected : pandas dataframe
            Dataframe with selected features
        """
        
        if self.selected_features == None:
            message = 'You first need to use the fit() method to determine the selected features!'
            return(print(message))
        else:
            # Get selected features
            if isinstance(X, np.ndarray):
                #print("Selecting for np.ndarray")
                X_selected = X[:,[int(i) for i in self.selected_features]]
            elif isinstance(X, pd.DataFrame):                
                X_selected = X[self.selected_features]
            else:
                return(print(f'Cannot select features for type: {type(X)}'))
            return X_selected
    
    def get_methods(self, method_order):
        
        # Return feature selection methods in the order specified:
        ordered_methods = {}
        
        for method_label in method_order:
            
            if method_label == 'Constant Features':
                ordered_methods.update({method_label: constant_features})
            
            elif method_label == 'Correlated Features':
                ordered_methods.update({method_label: correlated_features})
            
            elif method_label == 'Relevant Features':
                ordered_methods.update({method_label: relevant_features})
                
            elif method_label == 'RFECV Features':
                ordered_methods.update({method_label: rfecv_features})
            
            elif method_label == 'ANOVA Features':
                ordered_methods.update({method_label: anova_features})
        
        return ordered_methods


def constant_features(X, array_dict, frac_constant_values = 0.90):
    """
    Identifies features that have a large fraction of constant values.
    
    
    Parameters
    ----------
    X : pandas dataframe
        A data set where each row is an observation and each column a feature.
    
    array_dict : dictionary
        For input ndarrays, stores the array column counts for selection. Important
        for bookkeeping as the X input changes the index
        
    frac_constant_values: float, optional (default = 0.90)
        The threshold used to identify features with a large fraction of 
        constant values.
        
    Returns
    -------
    labels: list
        A list with the labels identifying the features that contain a 
        large fraction of constant values.
    """
    
    # Get number of rows in X
    num_rows = X.shape[0]
    
    # Get column labels
    if isinstance(X, np.ndarray):
        allLabels = [int(n) for n in array_dict['to_select']]# [str(n) for n in range(X.shape[1])]
        # Make a dict to store the fraction describing the value that occurs the most
        constant_per_feature = {label: max(np.unique(X[:,label], 
                                                     return_counts=True)[1]) / num_rows
                                for label in allLabels}
    else:
        allLabels = X.columns.tolist()
        # Make a dict to store the fraction describing the value that occurs the most
        constant_per_feature = {label: X[label].value_counts().iloc[0]/num_rows for label in allLabels}
    
    # Determine the features that contain a fraction of missing values greater than
    # the specified threshold
    labels = [label for label in allLabels if constant_per_feature [label] > frac_constant_values]
    
    return labels


def correlated_features(X, array_dict, correlation_threshold = 0.90):
    """
    Identifies features that are highly correlated. Let's assume that if
    two features or more are highly correlated, we can randomly select
    one of them and discard the rest without losing much information.
    
    
    Parameters
    ----------
    X : pandas dataframe
        A data set where each row is an observation and each column a feature.
        
    correlation_threshold: float, optional (default = 0.90)
        The threshold used to identify highly correlated features.
        
    Returns
    -------
    labels: list
        A list with the labels identifying the features that contain a 
        large fraction of constant values.
    """
    
    # Make correlation matrix
    if isinstance(X, np.ndarray):
        corr_matrix, pval = stats.spearmanr(X)#.abs()
        corr_matrix = np.absolute(corr_matrix)
        del pval
        upper = np.triu(corr_matrix)
        array_columns = [int(n) for n in array_dict['to_select']]
        # Find index of feature columns with correlation greater than correlation_threshold
        labels = [column for column in array_columns if any(upper[column] >  correlation_threshold)]
    else:
        corr_matrix = X.corr(method = "spearman").abs()
        # Select upper triangle of matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k = 1).astype(np.bool))    
        # Find index of feature columns with correlation greater than correlation_threshold
        labels = [column for column in upper.columns if any(upper[column] >  correlation_threshold)]
    
    return labels


def relevant_features(X, array_dict, y, params):
    """
    Determines the subset of features in X that are relevant to the outcome
    using the Boruta algorithm. The result are cross validated. 
        
    Parameters
    ----------
    X : pandas dataframe
        A data set where each row is an observation and each column a feature.
        
    y: numpy array
        A numpy array containing the targets
    
    params: dict,
        A dictionary containing the set of parameters use to initialize BorutaPy
        and determine the number of folds to use to validate the results.
    
    
    Examples
    --------
    # Initialize estimator
    estimator = RandomForestClassifier()
    
    # Define cv and BorutaPy parameters
     params = {'estimator': estimator,
               'cv': 5,
               'n_estimators': 1000,
               'max_iter': 100,
               'verbose': 50,
               'random_state': 42}
     
    # Get relevant feature labels
    labels = relevant_features(X = X, y = y, params = params)
    
    
    Returns
    -----
    labels: list
        A list with the labels identifying the relevant features in X.
    
    
    References
    ----------
    Find more details about Boruta here:
    https://github.com/scikit-learn-contrib/boruta_py
    
    """
    
    # Unpack params
    if 'cv' in params:
        cv = params['cv']
    else:
        cv = 5
    
    # Remove cv key from params so we can use with BorutaPy
    del params['cv']
    
    # Initiate variables
    feature_labels = list(X.columns)
    selected_features_mask = np.ones(len(feature_labels))
    counter = 0
      
    #Get K-folds indices
    kf = KFold(n_splits = cv)
    kf.get_n_splits(X)
    
    # Initiate progress bar
    status.printProgressBar(counter, cv, prefix = 'Progress:', 
                            suffix = 'Complete', length = 50)
    
    # K-fold cross validation
    for train_index, val_index in kf.split(X):
        # Get train fold data
        X_train_fold = X.iloc[train_index, :]
        y_train_fold = y[train_index]
        
        # Define Boruta feature selection method
        feat_selector = BorutaPy(**params)
        
        # Find all relevant features
        feat_selector.fit(X_train_fold.values, y_train_fold)
        
        # Boruta selected feature mask
        selected_features_temp = feat_selector.support_
        
        # Update selected relevant features
        selected_features_mask = selected_features_mask*selected_features_temp
        
        # Update progress bar
        counter += 1
        status.printProgressBar(counter, cv, prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    # Boruta selected feature labels
    labels = [feature_labels[ii] for ii in range(len(feature_labels)) if  selected_features_mask[ii] == 1]
    
    return labels


def rfecv_features(X, y, array_dict, rfecv_params):
    """
    Feature ranking with recursive feature elimination and cross-validated 
    selection of the best number of features. Determines the minimum number
    of features that are needed to maxmize the model's performance. 
    
    Parameters
    ----------
    X : pandas dataframe
        A data set where each row is an observation and each column a feature.
        
    y: numpy array
        A numpy array containing the targets
    
    rfecv_params: dict,
        A dictionary containing the set of parameters use to initialize RFECV sklearn
        class.
    
    
    Examples
    --------
    # Initialize estimator
    estimator = RandomForestClassifier()
    
    # Define RFECV parameters
    rfecv_params = {'estimator': estimator,
                    'cv': 2,
                    'step': 1,
                    'scoring': 'accuracy',
                    'verbose': 50}
    
    # Get rfecv feature labels
    labels = rfecv_features(X = X, y = y, rfecv_params = rfecv_params)
    
    
    Returns
    -----
    labels: list
        A list with the labels identifying the subset of features needed
        to maximize the model's performance.
    
    feature_selector: fitted RFECV object
    
    
    References
    ----------
    Find more details about Boruta here:
    https://github.com/scikit-learn-contrib/boruta_py
    
    """
    
    # Updating step based on percentage removal
    n_step = math.ceil(0.05 * X.shape[1]) #Based on column percentage
    if n_step < 1:
        n_step = 1
    rfecv_params['step'] = n_step
    print(f'Removal step count: {n_step}')
    
    # Initialize RFECV object
    feature_selector = RFECV(**rfecv_params)
    
    # Fit RFECV
    feature_selector.fit(X, y)
    
    # Get selected features
    if isinstance(X, np.ndarray):
        feature_labels = [int(i) for i in array_dict['to_select']]
        labels = [str(i) for (i, v) in zip(feature_labels, feature_selector.support_) if v]
    else:
        feature_labels = X.columns
        # Get selected features
        labels = feature_labels[feature_selector.support_].tolist()
    
    return labels, feature_selector

def anova_features(X, y, array_dict, anova_params):
    #Initialize selector object
    selection = SelectPercentile(**anova_params)
    #Fit Selector
    selection.fit_transform(X, y)
    #Get full column list
    if isinstance(X, np.ndarray):
        columns = np.asarray([int(i) for i in array_dict['to_select']])
    else:
        columns = np.asarray(X.columns.values)
    #Get boolean array of selected features
    support = np.asarray(selection.get_support())
    #Subset full list to selected features list
    columns_with_support = columns[support]
    
    return columns_with_support

class status:
    """  Report progress of process. """
    
    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        """
        Call in a loop to create terminal progress bar
        
        Parameters
        ----------
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
            
        Examples
        --------
        from time import sleep
        # A List of Items
        items = list(range(0, 57))
        l = len(items)
        
        # Initial call to print 0% progress
        printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i, item in enumerate(items):
            # Do stuff...
            sleep(0.1)
            # Update Progress Bar
            printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            
        References
        ----------
        Original Source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
        """
        
        
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()