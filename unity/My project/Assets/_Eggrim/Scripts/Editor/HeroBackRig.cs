using UnityEngine;
using UnityEditor;

public class HeroBackRig
{
    const string Folder = "Assets/_Eggrim/Art/Hero/Back";
    const float CanvasWidth = 24f;
    const float CanvasHeight = 48f;

    class Part
    {
        public string Name;
        public Rect OnCanvas;
    }

    static readonly Part[] PartsBackToFront =
    {
        new Part { Name = "leg_right", OnCanvas = new Rect(12, 33, 5, 15) },
        new Part { Name = "leg_left", OnCanvas = new Rect(7, 33, 5, 15) },
        new Part { Name = "body", OnCanvas = new Rect(7, 17, 10, 18) },
        new Part { Name = "hand_right", OnCanvas = new Rect(15, 17, 8, 19) },
        new Part { Name = "hand_left", OnCanvas = new Rect(1, 17, 8, 19) },
        new Part { Name = "head", OnCanvas = new Rect(2, 3, 21, 17) },
    };

    static readonly Vector2 CanvasBottomMiddle = new Vector2(CanvasWidth / 2f, CanvasHeight);

    [MenuItem("Eggrim/Build Back Rig")]
    public static void Build()
    {
        foreach (Part part in PartsBackToFront)
        {
            SpriteImportPreset.Apply($"{Folder}/readmey_back_{part.Name}.png");
        }

        GameObject hero = new GameObject("Hero");
        hero.AddComponent<Hero>();
        GameObject back = new GameObject("Back");
        back.transform.SetParent(hero.transform);

        int drawOrder = 0;
        foreach (Part part in PartsBackToFront)
        {
            SpritesHelper.AddPartSprite(back, part.Name, $"{Folder}/readmey_back_{part.Name}.png", part.OnCanvas, drawOrder);
            drawOrder += 1;
        }

        SerializedObject heroState = new SerializedObject(hero.GetComponent<Hero>());
        heroState.FindProperty("facingFront").objectReferenceValue = back;
        Undo.RegisterCreatedObjectUndo(hero, "Build Back Rig");
        Selection.activeGameObject = hero;
    }
}