using UnityEditor;
using UnityEngine;

public static class SpriteImportPreset
{
    [MenuItem("Eggrim/Apply Pixel Import Preset To Selection")]
    public static void ApplyToSelection()
    {
        foreach (Object obj in Selection.objects)
        {
            if (obj is Texture2D)
            {
                Apply(AssetDatabase.GetAssetPath(obj));
            }
        }
    }

    [MenuItem("Eggrim/Apply Pixel Import Preset To _Eggrim Art")]
    public static void ApplyToAllArt()
    {
        Apply("Assets/_Eggrim/Art");
    }

    private static void Apply(string folder)
    {
        foreach (string guid in AssetDatabase.FindAssets("t:Texture2D", new[] { folder }))
        {
            Apply(AssetDatabase.GUIDToAssetPath(guid));
        }
    }

    private static void Apply(string path)
    {
        TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
        if (importer == null)
        {
            return;
        }
        importer.filterMode = FilterMode.Point;
        importer.mipmapEnabled = false;
        importer.textureCompression = TextureImporterCompression.Uncompressed;
        importer.alphaIsTransparency = true;
        importer.spritePixelsPerUnit = 1f;
        importer.spriteImportMode = SpriteImportMode.Single;
        importer.SaveAndReimport();
    }
}