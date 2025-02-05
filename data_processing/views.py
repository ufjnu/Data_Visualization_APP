import plotly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from sklearn.decomposition import PCA
import pandas as pd
import plotly.express as px
import json


class DimensionalityReduction(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # 获取上传的文件
        file_obj = request.FILES['file']

        # 用 Pandas 读取 CSV 文件
        try:
            df = pd.read_csv(file_obj)
        except Exception as e:
            return Response({"error": f"Error reading CSV file: {e}"}, status=400)

        # 检查是否有足够的列进行降维
        if df.shape[1] < 4:  # 至少需要 4 维数据才能降维到 3D
            return Response({"error": "CSV file must have at least 4 columns for dimensionality reduction."},
                            status=400)

        # 进行降维处理
        try:
            pca = PCA(n_components=3)  # 降维到 3 维
            reduced_data = pca.fit_transform(df.values)
        except Exception as e:
            return Response({"error": f"Error during dimensionality reduction: {e}"}, status=500)

        # 将降维后的数据转换为 DataFrame
        reduced_df = pd.DataFrame(reduced_data, columns=['Dimension 1', 'Dimension 2', 'Dimension 3'])

        # 图表 1：降维后数据的 3D 散点图
        scatter_3d = px.scatter_3d(
            reduced_df,
            x='Dimension 1',
            y='Dimension 2',
            z='Dimension 3',
            title="3D Scatter Plot (Reduced Data)"
        )

        # 将图表对象转为 JSON 格式
        scatter_3d_json = json.dumps(scatter_3d, cls=plotly.utils.PlotlyJSONEncoder)

        return Response({"scatter_3d": scatter_3d_json})





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
import pandas as pd
import os
import json

@csrf_exempt
def dimensionality_reduction(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            method = data.get("method", "pca")
            n_components = int(data.get("n_components", 2))

            # 假设文件路径存储为 uploaded.csv
            file_path = os.path.join("media", "uploaded.csv")
            if not os.path.exists(file_path):
                return JsonResponse({"error": "No uploaded dataset found."}, status=404)

            df = pd.read_csv(file_path)

            if df.shape[1] < n_components:
                return JsonResponse({"error": "Number of components exceeds dataset dimensions."}, status=400)

            # 根据选择的方法进行降维
            if method == "pca":
                reducer = PCA(n_components=n_components)
            elif method == "tsne":
                reducer = TSNE(n_components=n_components)
            elif method == "umap":
                reducer = umap.UMAP(n_components=n_components)
            else:
                return JsonResponse({"error": "Invalid method selected."}, status=400)

            reduced_data = reducer.fit_transform(df.values)
            reduced_df = pd.DataFrame(reduced_data, columns=[f"Component {i+1}" for i in range(n_components)])

            # 保存降维后的数据集
            reduced_file_path = os.path.join("media", "reduced_data.csv")
            reduced_df.to_csv(reduced_file_path, index=False)

            return JsonResponse({"dataset": reduced_df.to_dict(orient="records")})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
