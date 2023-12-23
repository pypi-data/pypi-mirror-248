import os
import pandas as pd
import random
from Stabdifspy.Library.StabdifspyGlobals import StabdifspyGlobal

class Prompter:

    """
    プロンプト生成クラス
    """ 
    
    def __init__(self, _gv:StabdifspyGlobal, _rootPath):
        """
        コンストラクタ
        """

        # ルートパスを取得
        self.rootPath = _rootPath
    
        # 共通設定取得
        self.gv = _gv

    def getPromptFilePath(self):
        """
        Promptファイルパスを取得する
        """
        
        # Promptファイルパス
        return os.path.join(os.path.dirname(self.rootPath), self.gv.StabdifspyConfig.promptExcelPath)
        
    def getPositivePrompt(self):
        """
        Positiveプロンプトを生成する
        """
        
        # Promptファイルパス
        promptFilePath = self.getPromptFilePath()

        # Promptファイル読込⇒Dataframe変換(ComposeD)
        dfComposeD = pd.read_excel(promptFilePath, engine='openpyxl', sheet_name='ComposeD')
        
        # Promptファイル読込⇒Dataframe変換(Positiveプロンプト)
        dfPositives = pd.read_excel(promptFilePath, engine='openpyxl', sheet_name='Positive')

        # 生成プロンプトリスト(トークン単位で保持)
        positiveList = []

        # ComposeDシートの内容をループしてPositiveプロンプトをリスト化する
        for _, rowComposeD in dfComposeD.iterrows():
            
            # DetailCdごとのプロンプトリスト
            positiveSubList = []
            
            # 必須プロンプトを取得
            ppw1 = (dfPositives['DetailCd'] == rowComposeD['DetailCd']) & (dfPositives['Require'] == '*') & (dfPositives['ignore'] != '*')
            dfPositiveR:pd.DataFrame = dfPositives[ppw1]
            for _, rowPositive in dfPositiveR.iterrows():
                positiveSubList.append(rowPositive['Prompt'])

            # 最小プロンプト数取得
            minPromptCount = int(rowComposeD['MinElement'])
            # 最大プロンプト数取得
            maxPromptCount = int(rowComposeD['MaxElement'])
            
            # 追加プロンプト取得
            # 必須プロンプトが最小プロンプト数よりも下回っているか
            modPromptCount = len(positiveSubList) - random.randrange(minPromptCount, maxPromptCount + 1, 1)
            if (modPromptCount < 0):
                
                # ランダム取得するプロンプト数取得
                modPromptCount = abs(modPromptCount)

                # ランダムプロンプト対象取得
                ppw2 = (dfPositives['DetailCd'] == rowComposeD['DetailCd']) & (dfPositives['Require'] != '*') & (dfPositives['ignore'] != '*')
                dfPositiveSR:pd.DataFrame = dfPositives[ppw2]
                if (len(dfPositiveSR) > 0):
                    # 追加プロンプトをランダム抽出
                    dfPositiveSR = dfPositiveSR.sample(n=(modPromptCount))
                    for _, rowPositiveSR in dfPositiveSR.iterrows():
                        positiveSubList.append(rowPositiveSR['Prompt'])
            
            # プロンプトリスト追加
            positiveList.extend(positiveSubList)

        # 戻り値を返す
        return positiveList

    def getNegativePrompt(self):
        """
        Negativeプロンプトを生成する
        """

        # Promptファイルパス
        promptFilePath = self.getPromptFilePath()

        # Promptファイル読込⇒Dataframe変換(Negativeプロンプト)
        dfNegatives = pd.read_excel(promptFilePath, engine='openpyxl', sheet_name='Negative')
        
        # 生成プロンプトリスト(トークン単位で保持)
        negativeList = []
        
        # 必須プロンプトを取得
        npw1 = (dfNegatives['Require'] == '*') & (dfNegatives['ignore'] != '*')
        dfNegativeR:pd.DataFrame = dfNegatives[npw1]
        for _, rowNegative in dfNegativeR.iterrows():
            negativeList.append(rowNegative['Prompt'])
        
        # 戻り値を返す
        return negativeList
