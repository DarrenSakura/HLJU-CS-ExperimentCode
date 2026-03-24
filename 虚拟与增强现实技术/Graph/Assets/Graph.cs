using System;
using System.Collections;
using System.Collections.Generic;
using System.Drawing;
using UnityEngine;
public class Math : MonoBehaviour
{
    public Transform pointPrefab;
    public int resolution = 100;
    Transform[] points;
    public GraphFunctionName functionName;
    static GraphFunction[] functions =
    {
        SineFunction,
        MultiSineFunction,
        Sine2DFunction,
        MultiSine2DFunction,
        RippleFunction
    };
    // Start is called before the first frame update
    void Start()
    {
        Application.targetFrameRate = 120;
        float step = 2f / resolution;
        Vector3 scale = Vector3.one * step;
        points = new Transform[resolution * resolution];
        for (int i = 0; i < points.Length; i++)
        {
            Transform point = Instantiate(pointPrefab);
            point.localScale = scale;
            point.SetParent(transform, false);
            points[i] = point;
        }
    }
    // Update is called once per frame
    void Update()
    {
        float t = Time.time;
        GraphFunction f = functions[(int)functionName];
        float step = 2f / resolution;
        for (int i = 0, z = 0; z < resolution; z++)
        {            float v = (z + 0.5f) * step - 1f;
            for (int x = 0; x < resolution; x++, i++)
            {
                float u = (x + 0.5f) * step - 1f;
                points[i].localPosition = f(u, v, t);
            }
        }
    }
    static Vector3 SineFunction(float x, float z, float t)
    {
        Vector3 p;
        p.x = x;
        p.y = Mathf.Sin(MathF.PI * (x + t));
        p.z = z;
        return p;
    }
    static Vector3 Sine2DFunction(float x, float z, float t)
    {
        Vector3 p;
        p.x = x;
        p.y = Mathf.Sin(MathF.PI * (x + t));
        p.y += Mathf.Sin(MathF.PI * (z + t));
        p.y *= 0.5f;
        p.z = z;
        return p;
    }
    static Vector3 MultiSineFunction(float x, float z, float t)
    {
        Vector3 p;
        p.x = x;
        p.y = Mathf.Sin(Mathf.PI * (x + t));
        p.y += Mathf.Sin(Mathf.PI * (2f * x + t)) * 0.5f;
        p.y *= 2f / 3f;
        p.z = z;
        return p;
    }
    static Vector3 MultiSine2DFunction(float x, float z, float t)
    {
        Vector3 p;
        p.x = x;
        p.y = 4f * Mathf.Sin(Mathf.PI * (x + z + t * 0.5f));
        p.y += Mathf.Sin(Mathf.PI * (x + t));
        p.y += Mathf.Sin(2f*Mathf.PI * (z+2f* t)) * 0.5f;
        p.y *= 1f / 5.5f;
        p.z = z;
        return p;
    }
    static Vector3 RippleFunction(float x, float z, float t)
    {
        Vector3 p;
        float d = Mathf.Sqrt(x * x + z * z);
        p.x = x;
        p.y = Mathf.Sin(Mathf.PI * (4f * d - t));
        p.y /= 1f + 10f * d;
        p.z = z;
        return p;
    }
}