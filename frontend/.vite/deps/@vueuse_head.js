import {
  createHooks
} from "./chunk-3LJAMMO3.js";
import {
  defineComponent,
  getCurrentInstance,
  inject,
  nextTick,
  onActivated,
  onBeforeUnmount,
  onDeactivated,
  ref,
  unref,
  version,
  watch,
  watchEffect
} from "./chunk-IJV5NOMV.js";

// node_modules/packrup/dist/index.mjs
function unpackToArray(input, options) {
  const unpacked = [];
  const kFn = options.resolveKeyData || ((ctx) => ctx.key);
  const vFn = options.resolveValueData || ((ctx) => ctx.value);
  for (const [k2, v] of Object.entries(input)) {
    unpacked.push(...(Array.isArray(v) ? v : [v]).map((i) => {
      const ctx = { key: k2, value: i };
      const val = vFn(ctx);
      if (typeof val === "object")
        return unpackToArray(val, options);
      if (Array.isArray(val))
        return val;
      return {
        [typeof options.key === "function" ? options.key(ctx) : options.key]: kFn(ctx),
        [typeof options.value === "function" ? options.value(ctx) : options.value]: val
      };
    }).flat());
  }
  return unpacked;
}
function unpackToString(value, options) {
  return Object.entries(value).map(([key, value2]) => {
    if (typeof value2 === "object")
      value2 = unpackToString(value2, options);
    if (options.resolve) {
      const resolved = options.resolve({ key, value: value2 });
      if (typeof resolved !== "undefined")
        return resolved;
    }
    if (typeof value2 === "number")
      value2 = value2.toString();
    if (typeof value2 === "string" && options.wrapValue) {
      value2 = value2.replace(new RegExp(options.wrapValue, "g"), `\\${options.wrapValue}`);
      value2 = `${options.wrapValue}${value2}${options.wrapValue}`;
    }
    return `${key}${options.keyValueSeparator || ""}${value2}`;
  }).join(options.entrySeparator || "");
}

// node_modules/@unhead/shared/dist/index.mjs
var SelfClosingTags = /* @__PURE__ */ new Set(["meta", "link", "base"]);
var TagsWithInnerContent = /* @__PURE__ */ new Set(["title", "titleTemplate", "script", "style", "noscript"]);
var HasElementTags = /* @__PURE__ */ new Set([
  "base",
  "meta",
  "link",
  "style",
  "script",
  "noscript"
]);
var ValidHeadTags = /* @__PURE__ */ new Set([
  "title",
  "titleTemplate",
  "templateParams",
  "base",
  "htmlAttrs",
  "bodyAttrs",
  "meta",
  "link",
  "style",
  "script",
  "noscript"
]);
var UniqueTags = /* @__PURE__ */ new Set(["base", "title", "titleTemplate", "bodyAttrs", "htmlAttrs", "templateParams"]);
var TagConfigKeys = /* @__PURE__ */ new Set(["tagPosition", "tagPriority", "tagDuplicateStrategy", "children", "innerHTML", "textContent", "processTemplateParams"]);
var IsBrowser = typeof window !== "undefined";
var composableNames = [
  "getActiveHead",
  "useHead",
  "useSeoMeta",
  "useHeadSafe",
  "useServerHead",
  "useServerSeoMeta",
  "useServerHeadSafe"
];
function defineHeadPlugin(plugin) {
  return plugin;
}
function hashCode(s) {
  let h = 9;
  for (let i = 0; i < s.length; )
    h = Math.imul(h ^ s.charCodeAt(i++), 9 ** 9);
  return ((h ^ h >>> 9) + 65536).toString(16).substring(1, 8).toLowerCase();
}
function hashTag(tag) {
  if (tag._h) {
    return tag._h;
  }
  if (tag._d) {
    return hashCode(tag._d);
  }
  let content = `${tag.tag}:${tag.textContent || tag.innerHTML || ""}:`;
  for (const key in tag.props) {
    content += `${key}:${String(tag.props[key])},`;
  }
  return hashCode(content);
}
var p = (p2) => ({ keyValue: p2, metaKey: "property" });
var k = (p2) => ({ keyValue: p2 });
var MetaPackingSchema = {
  appleItunesApp: {
    unpack: {
      entrySeparator: ", ",
      resolve({ key, value }) {
        return `${fixKeyCase(key)}=${value}`;
      }
    }
  },
  articleExpirationTime: p("article:expiration_time"),
  articleModifiedTime: p("article:modified_time"),
  articlePublishedTime: p("article:published_time"),
  bookReleaseDate: p("book:release_date"),
  charset: {
    metaKey: "charset"
  },
  contentSecurityPolicy: {
    unpack: {
      entrySeparator: "; ",
      resolve({ key, value }) {
        return `${fixKeyCase(key)} ${value}`;
      }
    },
    metaKey: "http-equiv"
  },
  contentType: {
    metaKey: "http-equiv"
  },
  defaultStyle: {
    metaKey: "http-equiv"
  },
  fbAppId: p("fb:app_id"),
  msapplicationConfig: k("msapplication-Config"),
  msapplicationTileColor: k("msapplication-TileColor"),
  msapplicationTileImage: k("msapplication-TileImage"),
  ogAudioSecureUrl: p("og:audio:secure_url"),
  ogAudioUrl: p("og:audio"),
  ogImageSecureUrl: p("og:image:secure_url"),
  ogImageUrl: p("og:image"),
  ogSiteName: p("og:site_name"),
  ogVideoSecureUrl: p("og:video:secure_url"),
  ogVideoUrl: p("og:video"),
  profileFirstName: p("profile:first_name"),
  profileLastName: p("profile:last_name"),
  profileUsername: p("profile:username"),
  refresh: {
    metaKey: "http-equiv",
    unpack: {
      entrySeparator: ";",
      resolve({ key, value }) {
        if (key === "seconds")
          return `${value}`;
      }
    }
  },
  robots: {
    unpack: {
      entrySeparator: ", ",
      resolve({ key, value }) {
        if (typeof value === "boolean")
          return `${fixKeyCase(key)}`;
        else
          return `${fixKeyCase(key)}:${value}`;
      }
    }
  },
  xUaCompatible: {
    metaKey: "http-equiv"
  }
};
var openGraphNamespaces = /* @__PURE__ */ new Set([
  "og",
  "book",
  "article",
  "profile"
]);
function resolveMetaKeyType(key) {
  var _a;
  const fKey = fixKeyCase(key);
  const prefixIndex = fKey.indexOf(":");
  if (openGraphNamespaces.has(fKey.substring(0, prefixIndex)))
    return "property";
  return ((_a = MetaPackingSchema[key]) == null ? void 0 : _a.metaKey) || "name";
}
function resolveMetaKeyValue(key) {
  var _a;
  return ((_a = MetaPackingSchema[key]) == null ? void 0 : _a.keyValue) || fixKeyCase(key);
}
function fixKeyCase(key) {
  const updated = key.replace(/([A-Z])/g, "-$1").toLowerCase();
  const prefixIndex = updated.indexOf("-");
  const fKey = updated.substring(0, prefixIndex);
  if (fKey === "twitter" || openGraphNamespaces.has(fKey))
    return key.replace(/([A-Z])/g, ":$1").toLowerCase();
  return updated;
}
function changeKeyCasingDeep(input) {
  if (Array.isArray(input)) {
    return input.map((entry) => changeKeyCasingDeep(entry));
  }
  if (typeof input !== "object" || Array.isArray(input))
    return input;
  const output = {};
  for (const key in input) {
    if (!Object.prototype.hasOwnProperty.call(input, key)) {
      continue;
    }
    output[fixKeyCase(key)] = changeKeyCasingDeep(input[key]);
  }
  return output;
}
function resolvePackedMetaObjectValue(value, key) {
  const definition = MetaPackingSchema[key];
  if (key === "refresh")
    return `${value.seconds};url=${value.url}`;
  return unpackToString(
    changeKeyCasingDeep(value),
    {
      keyValueSeparator: "=",
      entrySeparator: ", ",
      resolve({ value: value2, key: key2 }) {
        if (value2 === null)
          return "";
        if (typeof value2 === "boolean")
          return `${key2}`;
      },
      ...definition == null ? void 0 : definition.unpack
    }
  );
}
var ObjectArrayEntries = /* @__PURE__ */ new Set(["og:image", "og:video", "og:audio", "twitter:image"]);
function sanitize(input) {
  const out = {};
  for (const k2 in input) {
    if (!Object.prototype.hasOwnProperty.call(input, k2)) {
      continue;
    }
    const v = input[k2];
    if (String(v) !== "false" && k2)
      out[k2] = v;
  }
  return out;
}
function handleObjectEntry(key, v) {
  const value = sanitize(v);
  const fKey = fixKeyCase(key);
  const attr = resolveMetaKeyType(fKey);
  if (ObjectArrayEntries.has(fKey)) {
    const input = {};
    for (const k2 in value) {
      if (!Object.prototype.hasOwnProperty.call(value, k2)) {
        continue;
      }
      input[`${key}${k2 === "url" ? "" : `${k2[0].toUpperCase()}${k2.slice(1)}`}`] = value[k2];
    }
    return unpackMeta(input).sort((a, b) => {
      var _a, _b;
      return (((_a = a[attr]) == null ? void 0 : _a.length) || 0) - (((_b = b[attr]) == null ? void 0 : _b.length) || 0);
    });
  }
  return [{ [attr]: fKey, ...value }];
}
function unpackMeta(input) {
  const extras = [];
  const primitives = {};
  for (const key in input) {
    if (!Object.prototype.hasOwnProperty.call(input, key)) {
      continue;
    }
    const value = input[key];
    if (!Array.isArray(value)) {
      if (typeof value === "object" && value) {
        if (ObjectArrayEntries.has(fixKeyCase(key))) {
          extras.push(...handleObjectEntry(key, value));
          continue;
        }
        primitives[key] = sanitize(value);
      } else {
        primitives[key] = value;
      }
      continue;
    }
    for (const v of value) {
      extras.push(...typeof v === "string" ? unpackMeta({ [key]: v }) : handleObjectEntry(key, v));
    }
  }
  const meta = unpackToArray(primitives, {
    key({ key }) {
      return resolveMetaKeyType(key);
    },
    value({ key }) {
      return key === "charset" ? "charset" : "content";
    },
    resolveKeyData({ key }) {
      return resolveMetaKeyValue(key);
    },
    resolveValueData({ value, key }) {
      if (value === null)
        return "_null";
      if (typeof value === "object")
        return resolvePackedMetaObjectValue(value, key);
      return typeof value === "number" ? value.toString() : value;
    }
  });
  return [...extras, ...meta].map((m) => {
    if (m.content === "_null")
      m.content = null;
    return m;
  });
}
function thenable(val, thenFn) {
  if (val instanceof Promise) {
    return val.then(thenFn);
  }
  return thenFn(val);
}
function normaliseTag(tagName, input, e, normalizedProps) {
  const props = normalizedProps || normaliseProps(
    // explicitly check for an object
    // @ts-expect-error untyped
    typeof input === "object" && typeof input !== "function" && !(input instanceof Promise) ? { ...input } : { [tagName === "script" || tagName === "noscript" || tagName === "style" ? "innerHTML" : "textContent"]: input },
    tagName === "templateParams" || tagName === "titleTemplate"
  );
  if (props instanceof Promise) {
    return props.then((val) => normaliseTag(tagName, input, e, val));
  }
  const tag = {
    tag: tagName,
    props
  };
  for (const k2 of TagConfigKeys) {
    const val = tag.props[k2] !== void 0 ? tag.props[k2] : e[k2];
    if (val !== void 0) {
      if (!(k2 === "innerHTML" || k2 === "textContent" || k2 === "children") || TagsWithInnerContent.has(tag.tag)) {
        tag[k2 === "children" ? "innerHTML" : k2] = val;
      }
      delete tag.props[k2];
    }
  }
  if (tag.props.body) {
    tag.tagPosition = "bodyClose";
    delete tag.props.body;
  }
  if (tag.tag === "script") {
    if (typeof tag.innerHTML === "object") {
      tag.innerHTML = JSON.stringify(tag.innerHTML);
      tag.props.type = tag.props.type || "application/json";
    }
  }
  return Array.isArray(tag.props.content) ? tag.props.content.map((v) => ({ ...tag, props: { ...tag.props, content: v } })) : tag;
}
function normaliseStyleClassProps(key, v) {
  var _a;
  const sep = key === "class" ? " " : ";";
  if (v && typeof v === "object" && !Array.isArray(v)) {
    v = Object.entries(v).filter(([, v2]) => v2).map(([k2, v2]) => key === "style" ? `${k2}:${v2}` : k2);
  }
  return (_a = String(Array.isArray(v) ? v.join(sep) : v)) == null ? void 0 : _a.split(sep).filter((c) => Boolean(c.trim())).join(sep);
}
function nestedNormaliseProps(props, virtual, keys, startIndex) {
  for (let i = startIndex; i < keys.length; i += 1) {
    const k2 = keys[i];
    if (k2 === "class" || k2 === "style") {
      props[k2] = normaliseStyleClassProps(k2, props[k2]);
      continue;
    }
    if (props[k2] instanceof Promise) {
      return props[k2].then((val) => {
        props[k2] = val;
        return nestedNormaliseProps(props, virtual, keys, i);
      });
    }
    if (!virtual && !TagConfigKeys.has(k2)) {
      const v = String(props[k2]);
      const isDataKey = k2.startsWith("data-");
      if (v === "true" || v === "") {
        props[k2] = isDataKey ? "true" : true;
      } else if (!props[k2]) {
        if (isDataKey && v === "false")
          props[k2] = "false";
        else
          delete props[k2];
      }
    }
  }
}
function normaliseProps(props, virtual = false) {
  const resolvedProps = nestedNormaliseProps(props, virtual, Object.keys(props), 0);
  if (resolvedProps instanceof Promise) {
    return resolvedProps.then(() => props);
  }
  return props;
}
var TagEntityBits = 10;
function nestedNormaliseEntryTags(headTags, tagPromises, startIndex) {
  for (let i = startIndex; i < tagPromises.length; i += 1) {
    const tags = tagPromises[i];
    if (tags instanceof Promise) {
      return tags.then((val) => {
        tagPromises[i] = val;
        return nestedNormaliseEntryTags(headTags, tagPromises, i);
      });
    }
    if (Array.isArray(tags)) {
      headTags.push(...tags);
    } else {
      headTags.push(tags);
    }
  }
}
function normaliseEntryTags(e) {
  const tagPromises = [];
  const input = e.resolvedInput;
  for (const k2 in input) {
    if (!Object.prototype.hasOwnProperty.call(input, k2)) {
      continue;
    }
    const v = input[k2];
    if (v === void 0 || !ValidHeadTags.has(k2)) {
      continue;
    }
    if (Array.isArray(v)) {
      for (const props of v) {
        tagPromises.push(normaliseTag(k2, props, e));
      }
      continue;
    }
    tagPromises.push(normaliseTag(k2, v, e));
  }
  if (tagPromises.length === 0) {
    return [];
  }
  const headTags = [];
  return thenable(nestedNormaliseEntryTags(headTags, tagPromises, 0), () => headTags.map((t, i) => {
    t._e = e._i;
    e.mode && (t._m = e.mode);
    t._p = (e._i << TagEntityBits) + i;
    return t;
  }));
}
var WhitelistAttributes = {
  htmlAttrs: ["id", "class", "lang", "dir"],
  bodyAttrs: ["id", "class"],
  meta: ["id", "name", "property", "charset", "content"],
  noscript: ["id", "textContent"],
  script: ["id", "type", "textContent"],
  link: ["id", "color", "crossorigin", "fetchpriority", "href", "hreflang", "imagesrcset", "imagesizes", "integrity", "media", "referrerpolicy", "rel", "sizes", "type"]
};
function acceptDataAttrs(value) {
  const filtered = {};
  Object.keys(value || {}).filter((a) => a.startsWith("data-")).forEach((a) => {
    filtered[a] = value[a];
  });
  return filtered;
}
function whitelistSafeInput(input) {
  const filtered = {};
  Object.keys(input).forEach((key) => {
    const tagValue = input[key];
    if (!tagValue)
      return;
    switch (key) {
      // always safe
      case "title":
      case "titleTemplate":
      case "templateParams":
        filtered[key] = tagValue;
        break;
      case "htmlAttrs":
      case "bodyAttrs":
        filtered[key] = acceptDataAttrs(tagValue);
        WhitelistAttributes[key].forEach((a) => {
          if (tagValue[a])
            filtered[key][a] = tagValue[a];
        });
        break;
      // meta is safe, except for http-equiv
      case "meta":
        if (Array.isArray(tagValue)) {
          filtered[key] = tagValue.map((meta) => {
            const safeMeta = acceptDataAttrs(meta);
            WhitelistAttributes.meta.forEach((key2) => {
              if (meta[key2])
                safeMeta[key2] = meta[key2];
            });
            return safeMeta;
          }).filter((meta) => Object.keys(meta).length > 0);
        }
        break;
      // link tags we don't allow stylesheets, scripts, preloading, prerendering, prefetching, etc
      case "link":
        if (Array.isArray(tagValue)) {
          filtered[key] = tagValue.map((meta) => {
            const link = acceptDataAttrs(meta);
            WhitelistAttributes.link.forEach((key2) => {
              const val = meta[key2];
              if (key2 === "rel" && (val === "stylesheet" || val === "canonical" || val === "modulepreload" || val === "prerender" || val === "preload" || val === "prefetch"))
                return;
              if (key2 === "href") {
                if (val.includes("javascript:") || val.includes("data:"))
                  return;
                link[key2] = val;
              } else if (val) {
                link[key2] = val;
              }
            });
            return link;
          }).filter((link) => Object.keys(link).length > 1 && !!link.rel);
        }
        break;
      case "noscript":
        if (Array.isArray(tagValue)) {
          filtered[key] = tagValue.map((meta) => {
            const noscript = acceptDataAttrs(meta);
            WhitelistAttributes.noscript.forEach((key2) => {
              if (meta[key2])
                noscript[key2] = meta[key2];
            });
            return noscript;
          }).filter((meta) => Object.keys(meta).length > 0);
        }
        break;
      // we only allow JSON in scripts
      case "script":
        if (Array.isArray(tagValue)) {
          filtered[key] = tagValue.map((script) => {
            const safeScript = acceptDataAttrs(script);
            WhitelistAttributes.script.forEach((s) => {
              if (script[s]) {
                if (s === "textContent") {
                  try {
                    const jsonVal = typeof script[s] === "string" ? JSON.parse(script[s]) : script[s];
                    safeScript[s] = JSON.stringify(jsonVal, null, 0);
                  } catch (e) {
                  }
                } else {
                  safeScript[s] = script[s];
                }
              }
            });
            return safeScript;
          }).filter((meta) => Object.keys(meta).length > 0);
        }
        break;
    }
  });
  return filtered;
}
var NetworkEvents = /* @__PURE__ */ new Set(["onload", "onerror", "onabort", "onprogress", "onloadstart"]);
var TAG_WEIGHTS = {
  // tags
  base: -10,
  title: 10
};
var TAG_ALIASES = {
  // relative scores to their default values
  critical: -80,
  high: -10,
  low: 20
};
function tagWeight(tag) {
  const priority = tag.tagPriority;
  if (typeof priority === "number")
    return priority;
  let weight = 100;
  if (tag.tag === "meta") {
    if (tag.props["http-equiv"] === "content-security-policy")
      weight = -30;
    else if (tag.props.charset)
      weight = -20;
    else if (tag.props.name === "viewport")
      weight = -15;
  } else if (tag.tag === "link" && tag.props.rel === "preconnect") {
    weight = 20;
  } else if (tag.tag in TAG_WEIGHTS) {
    weight = TAG_WEIGHTS[tag.tag];
  }
  if (priority && priority in TAG_ALIASES) {
    return weight + TAG_ALIASES[priority];
  }
  return weight;
}
var SortModifiers = [{ prefix: "before:", offset: -1 }, { prefix: "after:", offset: 1 }];
var allowedMetaProperties = ["name", "property", "http-equiv"];
function tagDedupeKey(tag) {
  const { props, tag: tagName } = tag;
  if (UniqueTags.has(tagName))
    return tagName;
  if (tagName === "link" && props.rel === "canonical")
    return "canonical";
  if (props.charset)
    return "charset";
  if (props.id) {
    return `${tagName}:id:${props.id}`;
  }
  for (const n of allowedMetaProperties) {
    if (props[n] !== void 0) {
      return `${tagName}:${n}:${props[n]}`;
    }
  }
  return false;
}
var sepSub = "%separator";
function sub(p2, token, isJson = false) {
  var _a;
  let val;
  if (token === "s" || token === "pageTitle") {
    val = p2.pageTitle;
  } else if (token.includes(".")) {
    const dotIndex = token.indexOf(".");
    val = (_a = p2[token.substring(0, dotIndex)]) == null ? void 0 : _a[token.substring(dotIndex + 1)];
  } else {
    val = p2[token];
  }
  if (val !== void 0) {
    return isJson ? (val || "").replace(/"/g, '\\"') : val || "";
  }
  return void 0;
}
var sepSubRe = new RegExp(`${sepSub}(?:\\s*${sepSub})*`, "g");
function processTemplateParams(s, p2, sep, isJson = false) {
  if (typeof s !== "string" || !s.includes("%"))
    return s;
  let decoded = s;
  try {
    decoded = decodeURI(s);
  } catch {
  }
  const tokens = decoded.match(/%\w+(?:\.\w+)?/g);
  if (!tokens) {
    return s;
  }
  const hasSepSub = s.includes(sepSub);
  s = s.replace(/%\w+(?:\.\w+)?/g, (token) => {
    if (token === sepSub || !tokens.includes(token)) {
      return token;
    }
    const re = sub(p2, token.slice(1), isJson);
    return re !== void 0 ? re : token;
  }).trim();
  if (hasSepSub) {
    if (s.endsWith(sepSub))
      s = s.slice(0, -sepSub.length);
    if (s.startsWith(sepSub))
      s = s.slice(sepSub.length);
    s = s.replace(sepSubRe, sep).trim();
  }
  return s;
}
function resolveTitleTemplate(template, title) {
  if (template == null)
    return title || null;
  if (typeof template === "function")
    return template(title);
  return template;
}

// node_modules/@unhead/dom/dist/index.mjs
async function renderDOMHead(head, options = {}) {
  const dom = options.document || head.resolvedOptions.document;
  if (!dom || !head.dirty)
    return;
  const beforeRenderCtx = { shouldRender: true, tags: [] };
  await head.hooks.callHook("dom:beforeRender", beforeRenderCtx);
  if (!beforeRenderCtx.shouldRender)
    return;
  if (head._domUpdatePromise) {
    return head._domUpdatePromise;
  }
  head._domUpdatePromise = new Promise(async (resolve) => {
    var _a;
    const tags = (await head.resolveTags()).map((tag) => ({
      tag,
      id: HasElementTags.has(tag.tag) ? hashTag(tag) : tag.tag,
      shouldRender: true
    }));
    let state = head._dom;
    if (!state) {
      state = {
        elMap: { htmlAttrs: dom.documentElement, bodyAttrs: dom.body }
      };
      const takenDedupeKeys = /* @__PURE__ */ new Set();
      for (const key of ["body", "head"]) {
        const children = (_a = dom[key]) == null ? void 0 : _a.children;
        for (const c of children) {
          const tag = c.tagName.toLowerCase();
          if (!HasElementTags.has(tag)) {
            continue;
          }
          const t = {
            tag,
            props: await normaliseProps(
              c.getAttributeNames().reduce((props, name) => ({ ...props, [name]: c.getAttribute(name) }), {})
            ),
            innerHTML: c.innerHTML
          };
          const dedupeKey = tagDedupeKey(t);
          let d = dedupeKey;
          let i = 1;
          while (d && takenDedupeKeys.has(d))
            d = `${dedupeKey}:${i++}`;
          if (d) {
            t._d = d;
            takenDedupeKeys.add(d);
          }
          state.elMap[c.getAttribute("data-hid") || hashTag(t)] = c;
        }
      }
    }
    state.pendingSideEffects = { ...state.sideEffects };
    state.sideEffects = {};
    function track(id, scope, fn) {
      const k2 = `${id}:${scope}`;
      state.sideEffects[k2] = fn;
      delete state.pendingSideEffects[k2];
    }
    function trackCtx({ id, $el, tag }) {
      const isAttrTag = tag.tag.endsWith("Attrs");
      state.elMap[id] = $el;
      if (!isAttrTag) {
        if (tag.textContent && tag.textContent !== $el.textContent) {
          $el.textContent = tag.textContent;
        }
        if (tag.innerHTML && tag.innerHTML !== $el.innerHTML) {
          $el.innerHTML = tag.innerHTML;
        }
        track(id, "el", () => {
          var _a2;
          (_a2 = state.elMap[id]) == null ? void 0 : _a2.remove();
          delete state.elMap[id];
        });
      }
      if (tag._eventHandlers) {
        for (const k2 in tag._eventHandlers) {
          if (!Object.prototype.hasOwnProperty.call(tag._eventHandlers, k2)) {
            continue;
          }
          if ($el.getAttribute(`data-${k2}`) !== "") {
            (tag.tag === "bodyAttrs" ? dom.defaultView : $el).addEventListener(
              // onload -> load
              k2.substring(2),
              tag._eventHandlers[k2].bind($el)
            );
            $el.setAttribute(`data-${k2}`, "");
          }
        }
      }
      for (const k2 in tag.props) {
        if (!Object.prototype.hasOwnProperty.call(tag.props, k2)) {
          continue;
        }
        const value = tag.props[k2];
        const ck = `attr:${k2}`;
        if (k2 === "class") {
          if (!value) {
            continue;
          }
          for (const c of value.split(" ")) {
            isAttrTag && track(id, `${ck}:${c}`, () => $el.classList.remove(c));
            !$el.classList.contains(c) && $el.classList.add(c);
          }
        } else if (k2 === "style") {
          if (!value) {
            continue;
          }
          for (const c of value.split(";")) {
            const propIndex = c.indexOf(":");
            const k22 = c.substring(0, propIndex).trim();
            const v = c.substring(propIndex + 1).trim();
            track(id, `${ck}:${k22}`, () => {
              $el.style.removeProperty(k22);
            });
            $el.style.setProperty(k22, v);
          }
        } else {
          $el.getAttribute(k2) !== value && $el.setAttribute(k2, value === true ? "" : String(value));
          isAttrTag && track(id, ck, () => $el.removeAttribute(k2));
        }
      }
    }
    const pending = [];
    const frag = {
      bodyClose: void 0,
      bodyOpen: void 0,
      head: void 0
    };
    for (const ctx of tags) {
      const { tag, shouldRender, id } = ctx;
      if (!shouldRender)
        continue;
      if (tag.tag === "title") {
        dom.title = tag.textContent;
        continue;
      }
      ctx.$el = ctx.$el || state.elMap[id];
      if (ctx.$el) {
        trackCtx(ctx);
      } else if (HasElementTags.has(tag.tag)) {
        pending.push(ctx);
      }
    }
    for (const ctx of pending) {
      const pos = ctx.tag.tagPosition || "head";
      ctx.$el = dom.createElement(ctx.tag.tag);
      trackCtx(ctx);
      frag[pos] = frag[pos] || dom.createDocumentFragment();
      frag[pos].appendChild(ctx.$el);
    }
    for (const ctx of tags)
      await head.hooks.callHook("dom:renderTag", ctx, dom, track);
    frag.head && dom.head.appendChild(frag.head);
    frag.bodyOpen && dom.body.insertBefore(frag.bodyOpen, dom.body.firstChild);
    frag.bodyClose && dom.body.appendChild(frag.bodyClose);
    for (const k2 in state.pendingSideEffects) {
      state.pendingSideEffects[k2]();
    }
    head._dom = state;
    await head.hooks.callHook("dom:rendered", { renders: tags });
    resolve();
  }).finally(() => {
    head._domUpdatePromise = void 0;
    head.dirty = false;
  });
  return head._domUpdatePromise;
}
function debouncedRenderDOMHead(head, options = {}) {
  const fn = options.delayFn || ((fn2) => setTimeout(fn2, 10));
  return head._domDebouncedUpdatePromise = head._domDebouncedUpdatePromise || new Promise((resolve) => fn(() => {
    return renderDOMHead(head, options).then(() => {
      delete head._domDebouncedUpdatePromise;
      resolve();
    });
  }));
}
function DomPlugin(options) {
  return defineHeadPlugin((head) => {
    var _a, _b;
    const initialPayload = ((_b = (_a = head.resolvedOptions.document) == null ? void 0 : _a.head.querySelector('script[id="unhead:payload"]')) == null ? void 0 : _b.innerHTML) || false;
    if (initialPayload) {
      head.push(JSON.parse(initialPayload));
    }
    return {
      mode: "client",
      hooks: {
        "entries:updated": (head2) => {
          debouncedRenderDOMHead(head2, options);
        }
      }
    };
  });
}

// node_modules/unhead/dist/index.mjs
var UsesMergeStrategy = /* @__PURE__ */ new Set(["templateParams", "htmlAttrs", "bodyAttrs"]);
var DedupePlugin = defineHeadPlugin({
  hooks: {
    "tag:normalise": ({ tag }) => {
      if (tag.props.hid) {
        tag.key = tag.props.hid;
        delete tag.props.hid;
      }
      if (tag.props.vmid) {
        tag.key = tag.props.vmid;
        delete tag.props.vmid;
      }
      if (tag.props.key) {
        tag.key = tag.props.key;
        delete tag.props.key;
      }
      const generatedKey = tagDedupeKey(tag);
      if (generatedKey && !generatedKey.startsWith("meta:og:") && !generatedKey.startsWith("meta:twitter:")) {
        delete tag.key;
      }
      const dedupe = generatedKey || (tag.key ? `${tag.tag}:${tag.key}` : false);
      if (dedupe)
        tag._d = dedupe;
    },
    "tags:resolve": (ctx) => {
      const deduping = /* @__PURE__ */ Object.create(null);
      for (const tag of ctx.tags) {
        const dedupeKey = (tag.key ? `${tag.tag}:${tag.key}` : tag._d) || hashTag(tag);
        const dupedTag = deduping[dedupeKey];
        if (dupedTag) {
          let strategy = tag == null ? void 0 : tag.tagDuplicateStrategy;
          if (!strategy && UsesMergeStrategy.has(tag.tag))
            strategy = "merge";
          if (strategy === "merge") {
            const oldProps = dupedTag.props;
            if (oldProps.style && tag.props.style) {
              if (oldProps.style[oldProps.style.length - 1] !== ";") {
                oldProps.style += ";";
              }
              tag.props.style = `${oldProps.style} ${tag.props.style}`;
            }
            if (oldProps.class && tag.props.class) {
              tag.props.class = `${oldProps.class} ${tag.props.class}`;
            } else if (oldProps.class) {
              tag.props.class = oldProps.class;
            }
            deduping[dedupeKey].props = {
              ...oldProps,
              ...tag.props
            };
            continue;
          } else if (tag._e === dupedTag._e) {
            dupedTag._duped = dupedTag._duped || [];
            tag._d = `${dupedTag._d}:${dupedTag._duped.length + 1}`;
            dupedTag._duped.push(tag);
            continue;
          } else if (tagWeight(tag) > tagWeight(dupedTag)) {
            continue;
          }
        }
        const hasProps = tag.innerHTML || tag.textContent || Object.keys(tag.props).length !== 0;
        if (!hasProps && HasElementTags.has(tag.tag)) {
          delete deduping[dedupeKey];
          continue;
        }
        deduping[dedupeKey] = tag;
      }
      const newTags = [];
      for (const key in deduping) {
        const tag = deduping[key];
        const dupes = tag._duped;
        newTags.push(tag);
        if (dupes) {
          delete tag._duped;
          newTags.push(...dupes);
        }
      }
      ctx.tags = newTags;
      ctx.tags = ctx.tags.filter((t) => !(t.tag === "meta" && (t.props.name || t.props.property) && !t.props.content));
    }
  }
});
var ValidEventTags = /* @__PURE__ */ new Set(["script", "link", "bodyAttrs"]);
var EventHandlersPlugin = defineHeadPlugin((head) => ({
  hooks: {
    "tags:resolve": (ctx) => {
      for (const tag of ctx.tags) {
        if (!ValidEventTags.has(tag.tag)) {
          continue;
        }
        const props = tag.props;
        for (const key in props) {
          if (key[0] !== "o" || key[1] !== "n") {
            continue;
          }
          if (!Object.prototype.hasOwnProperty.call(props, key)) {
            continue;
          }
          const value = props[key];
          if (typeof value !== "function") {
            continue;
          }
          if (head.ssr && NetworkEvents.has(key)) {
            props[key] = `this.dataset.${key}fired = true`;
          } else {
            delete props[key];
          }
          tag._eventHandlers = tag._eventHandlers || {};
          tag._eventHandlers[key] = value;
        }
        if (head.ssr && tag._eventHandlers && (tag.props.src || tag.props.href)) {
          tag.key = tag.key || hashCode(tag.props.src || tag.props.href);
        }
      }
    },
    "dom:renderTag": ({ $el, tag }) => {
      var _a, _b;
      const dataset = $el == null ? void 0 : $el.dataset;
      if (!dataset) {
        return;
      }
      for (const k2 in dataset) {
        if (!k2.endsWith("fired")) {
          continue;
        }
        const ek = k2.slice(0, -5);
        if (!NetworkEvents.has(ek)) {
          continue;
        }
        (_b = (_a = tag._eventHandlers) == null ? void 0 : _a[ek]) == null ? void 0 : _b.call($el, new Event(ek.substring(2)));
      }
    }
  }
}));
var DupeableTags = /* @__PURE__ */ new Set(["link", "style", "script", "noscript"]);
var HashKeyedPlugin = defineHeadPlugin({
  hooks: {
    "tag:normalise": ({ tag }) => {
      if (tag.key && DupeableTags.has(tag.tag)) {
        tag.props["data-hid"] = tag._h = hashCode(tag.key);
      }
    }
  }
});
var PayloadPlugin = defineHeadPlugin({
  mode: "server",
  hooks: {
    "tags:beforeResolve": (ctx) => {
      const payload = {};
      let hasPayload = false;
      for (const tag of ctx.tags) {
        if (tag._m !== "server" || tag.tag !== "titleTemplate" && tag.tag !== "templateParams" && tag.tag !== "title") {
          continue;
        }
        payload[tag.tag] = tag.tag === "title" || tag.tag === "titleTemplate" ? tag.textContent : tag.props;
        hasPayload = true;
      }
      if (hasPayload) {
        ctx.tags.push({
          tag: "script",
          innerHTML: JSON.stringify(payload),
          props: { id: "unhead:payload", type: "application/json" }
        });
      }
    }
  }
});
var SortPlugin = defineHeadPlugin({
  hooks: {
    "tags:resolve": (ctx) => {
      var _a;
      for (const tag of ctx.tags) {
        if (typeof tag.tagPriority !== "string") {
          continue;
        }
        for (const { prefix, offset } of SortModifiers) {
          if (!tag.tagPriority.startsWith(prefix)) {
            continue;
          }
          const key = tag.tagPriority.substring(prefix.length);
          const position = (_a = ctx.tags.find((tag2) => tag2._d === key)) == null ? void 0 : _a._p;
          if (position !== void 0) {
            tag._p = position + offset;
            break;
          }
        }
      }
      ctx.tags.sort((a, b) => {
        const aWeight = tagWeight(a);
        const bWeight = tagWeight(b);
        if (aWeight < bWeight) {
          return -1;
        } else if (aWeight > bWeight) {
          return 1;
        }
        return a._p - b._p;
      });
    }
  }
});
var SupportedAttrs = {
  meta: "content",
  link: "href",
  htmlAttrs: "lang"
};
var contentAttrs = ["innerHTML", "textContent"];
var TemplateParamsPlugin = defineHeadPlugin((head) => ({
  hooks: {
    "tags:resolve": (ctx) => {
      var _a;
      const { tags } = ctx;
      let templateParams;
      for (let i = 0; i < tags.length; i += 1) {
        const tag = tags[i];
        if (tag.tag !== "templateParams") {
          continue;
        }
        templateParams = ctx.tags.splice(i, 1)[0].props;
        i -= 1;
      }
      const params = templateParams || {};
      const sep = params.separator || "|";
      delete params.separator;
      params.pageTitle = processTemplateParams(
        // find templateParams
        params.pageTitle || ((_a = tags.find((tag) => tag.tag === "title")) == null ? void 0 : _a.textContent) || "",
        params,
        sep
      );
      for (const tag of tags) {
        if (tag.processTemplateParams === false) {
          continue;
        }
        const v = SupportedAttrs[tag.tag];
        if (v && typeof tag.props[v] === "string") {
          tag.props[v] = processTemplateParams(tag.props[v], params, sep);
        } else if (tag.processTemplateParams || tag.tag === "titleTemplate" || tag.tag === "title") {
          for (const p2 of contentAttrs) {
            if (typeof tag[p2] === "string")
              tag[p2] = processTemplateParams(tag[p2], params, sep, tag.tag === "script" && tag.props.type.endsWith("json"));
          }
        }
      }
      head._templateParams = params;
      head._separator = sep;
    },
    "tags:afterResolve": ({ tags }) => {
      let title;
      for (let i = 0; i < tags.length; i += 1) {
        const tag = tags[i];
        if (tag.tag === "title" && tag.processTemplateParams !== false) {
          title = tag;
        }
      }
      if (title == null ? void 0 : title.textContent) {
        title.textContent = processTemplateParams(title.textContent, head._templateParams, head._separator);
      }
    }
  }
}));
var TitleTemplatePlugin = defineHeadPlugin({
  hooks: {
    "tags:resolve": (ctx) => {
      const { tags } = ctx;
      let titleTag;
      let titleTemplateTag;
      for (let i = 0; i < tags.length; i += 1) {
        const tag = tags[i];
        if (tag.tag === "title") {
          titleTag = tag;
        } else if (tag.tag === "titleTemplate") {
          titleTemplateTag = tag;
        }
      }
      if (titleTemplateTag && titleTag) {
        const newTitle = resolveTitleTemplate(
          titleTemplateTag.textContent,
          titleTag.textContent
        );
        if (newTitle !== null) {
          titleTag.textContent = newTitle || titleTag.textContent;
        } else {
          ctx.tags.splice(ctx.tags.indexOf(titleTag), 1);
        }
      } else if (titleTemplateTag) {
        const newTitle = resolveTitleTemplate(
          titleTemplateTag.textContent
        );
        if (newTitle !== null) {
          titleTemplateTag.textContent = newTitle;
          titleTemplateTag.tag = "title";
          titleTemplateTag = void 0;
        }
      }
      if (titleTemplateTag) {
        ctx.tags.splice(ctx.tags.indexOf(titleTemplateTag), 1);
      }
    }
  }
});
var XSSPlugin = defineHeadPlugin({
  hooks: {
    "tags:afterResolve": (ctx) => {
      for (const tag of ctx.tags) {
        if (typeof tag.innerHTML === "string") {
          if (tag.innerHTML && (tag.props.type === "application/ld+json" || tag.props.type === "application/json")) {
            tag.innerHTML = tag.innerHTML.replace(/</g, "\\u003C");
          } else {
            tag.innerHTML = tag.innerHTML.replace(new RegExp(`</${tag.tag}`, "g"), `<\\/${tag.tag}`);
          }
        }
      }
    }
  }
});
var activeHead;
function createHead(options = {}) {
  const head = createHeadCore(options);
  head.use(DomPlugin());
  return activeHead = head;
}
function filterMode(mode, ssr) {
  return !mode || mode === "server" && ssr || mode === "client" && !ssr;
}
function createHeadCore(options = {}) {
  const hooks = createHooks();
  hooks.addHooks(options.hooks || {});
  options.document = options.document || (IsBrowser ? document : void 0);
  const ssr = !options.document;
  const updated = () => {
    head.dirty = true;
    hooks.callHook("entries:updated", head);
  };
  let entryCount = 0;
  let entries = [];
  const plugins = [];
  const head = {
    plugins,
    dirty: false,
    resolvedOptions: options,
    hooks,
    headEntries() {
      return entries;
    },
    use(p2) {
      const plugin = typeof p2 === "function" ? p2(head) : p2;
      if (!plugin.key || !plugins.some((p22) => p22.key === plugin.key)) {
        plugins.push(plugin);
        filterMode(plugin.mode, ssr) && hooks.addHooks(plugin.hooks || {});
      }
    },
    push(input, entryOptions) {
      entryOptions == null ? true : delete entryOptions.head;
      const entry = {
        _i: entryCount++,
        input,
        ...entryOptions
      };
      if (filterMode(entry.mode, ssr)) {
        entries.push(entry);
        updated();
      }
      return {
        dispose() {
          entries = entries.filter((e) => e._i !== entry._i);
          updated();
        },
        // a patch is the same as creating a new entry, just a nice DX
        patch(input2) {
          for (const e of entries) {
            if (e._i === entry._i) {
              e.input = entry.input = input2;
            }
          }
          updated();
        }
      };
    },
    async resolveTags() {
      const resolveCtx = { tags: [], entries: [...entries] };
      await hooks.callHook("entries:resolve", resolveCtx);
      for (const entry of resolveCtx.entries) {
        const resolved = entry.resolvedInput || entry.input;
        entry.resolvedInput = await (entry.transform ? entry.transform(resolved) : resolved);
        if (entry.resolvedInput) {
          for (const tag of await normaliseEntryTags(entry)) {
            const tagCtx = { tag, entry, resolvedOptions: head.resolvedOptions };
            await hooks.callHook("tag:normalise", tagCtx);
            resolveCtx.tags.push(tagCtx.tag);
          }
        }
      }
      await hooks.callHook("tags:beforeResolve", resolveCtx);
      await hooks.callHook("tags:resolve", resolveCtx);
      await hooks.callHook("tags:afterResolve", resolveCtx);
      return resolveCtx.tags;
    },
    ssr
  };
  [
    DedupePlugin,
    PayloadPlugin,
    EventHandlersPlugin,
    HashKeyedPlugin,
    SortPlugin,
    TemplateParamsPlugin,
    TitleTemplatePlugin,
    XSSPlugin,
    ...(options == null ? void 0 : options.plugins) || []
  ].forEach((p2) => head.use(p2));
  head.hooks.callHook("init", head);
  return head;
}
function getActiveHead() {
  return activeHead;
}
var ScriptProxyTarget = Symbol("ScriptProxyTarget");
function scriptProxy() {
}
scriptProxy[ScriptProxyTarget] = true;

// node_modules/@unhead/vue/dist/shared/vue.ziyDaVMR.mjs
var Vue3 = version[0] === "3";
function resolveUnref(r) {
  return typeof r === "function" ? r() : unref(r);
}
function resolveUnrefHeadInput(ref2) {
  if (ref2 instanceof Promise || ref2 instanceof Date || ref2 instanceof RegExp)
    return ref2;
  const root = resolveUnref(ref2);
  if (!ref2 || !root)
    return root;
  if (Array.isArray(root))
    return root.map((r) => resolveUnrefHeadInput(r));
  if (typeof root === "object") {
    const resolved = {};
    for (const k2 in root) {
      if (!Object.prototype.hasOwnProperty.call(root, k2)) {
        continue;
      }
      if (k2 === "titleTemplate" || k2[0] === "o" && k2[1] === "n") {
        resolved[k2] = unref(root[k2]);
        continue;
      }
      resolved[k2] = resolveUnrefHeadInput(root[k2]);
    }
    return resolved;
  }
  return root;
}
var VueReactivityPlugin = defineHeadPlugin({
  hooks: {
    "entries:resolve": (ctx) => {
      for (const entry of ctx.entries)
        entry.resolvedInput = resolveUnrefHeadInput(entry.input);
    }
  }
});
var headSymbol = "usehead";
function vueInstall(head) {
  const plugin = {
    install(app) {
      if (Vue3) {
        app.config.globalProperties.$unhead = head;
        app.config.globalProperties.$head = head;
        app.provide(headSymbol, head);
      }
    }
  };
  return plugin.install;
}
function createHead2(options = {}) {
  options.domDelayFn = options.domDelayFn || ((fn) => nextTick(() => setTimeout(() => fn(), 0)));
  const head = createHead(options);
  head.use(VueReactivityPlugin);
  head.install = vueInstall(head);
  return head;
}
var _global = typeof globalThis !== "undefined" ? globalThis : typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : {};
var globalKey = "__unhead_injection_handler__";
function injectHead() {
  if (globalKey in _global) {
    return _global[globalKey]();
  }
  const head = inject(headSymbol);
  if (!head && true)
    console.warn("Unhead is missing Vue context, falling back to shared context. This may have unexpected results.");
  return head || getActiveHead();
}

// node_modules/@unhead/vue/dist/shared/vue.-sixQ7xP.mjs
function useHead(input, options = {}) {
  const head = options.head || injectHead();
  if (head) {
    if (!head.ssr)
      return clientUseHead(head, input, options);
    return head.push(input, options);
  }
}
function clientUseHead(head, input, options = {}) {
  const deactivated = ref(false);
  const resolvedInput = ref({});
  watchEffect(() => {
    resolvedInput.value = deactivated.value ? {} : resolveUnrefHeadInput(input);
  });
  const entry = head.push(resolvedInput.value, options);
  watch(resolvedInput, (e) => {
    entry.patch(e);
  });
  const vm = getCurrentInstance();
  if (vm) {
    onBeforeUnmount(() => {
      entry.dispose();
    });
    onDeactivated(() => {
      deactivated.value = true;
    });
    onActivated(() => {
      deactivated.value = false;
    });
  }
  return entry;
}

// node_modules/@unhead/vue/dist/index.mjs
var coreComposableNames = [
  "injectHead"
];
var unheadVueComposablesImports = {
  "@unhead/vue": [...coreComposableNames, ...composableNames]
};
function useHeadSafe(input, options = {}) {
  return useHead(input, { ...options, transform: whitelistSafeInput });
}
function useSeoMeta(input, options) {
  const { title, titleTemplate, ...meta } = input;
  return useHead({
    title,
    titleTemplate,
    // @ts-expect-error runtime type
    _flatMeta: meta
  }, {
    ...options,
    transform(t) {
      const meta2 = unpackMeta({ ...t._flatMeta });
      delete t._flatMeta;
      return {
        // @ts-expect-error runtime type
        ...t,
        meta: meta2
      };
    }
  });
}
function useServerHead(input, options = {}) {
  const head = options.head || injectHead();
  delete options.head;
  if (head)
    return head.push(input, { ...options, mode: "server" });
}
function useServerHeadSafe(input, options = {}) {
  return useHeadSafe(input, { ...options, mode: "server" });
}
function useServerSeoMeta(input, options) {
  return useSeoMeta(input, { ...options, mode: "server" });
}
var Vue2ProvideUnheadPlugin = (_Vue, head) => {
  _Vue.mixin({
    beforeCreate() {
      const options = this.$options;
      const origProvide = options.provide;
      options.provide = function() {
        let origProvideResult;
        if (typeof origProvide === "function")
          origProvideResult = origProvide.call(this);
        else
          origProvideResult = origProvide || {};
        return {
          ...origProvideResult,
          [headSymbol]: head
        };
      };
    }
  });
};
var VueHeadMixin = {
  created() {
    let source = false;
    if (Vue3) {
      const instance = getCurrentInstance();
      if (!instance)
        return;
      const options = instance.type;
      if (!options || !("head" in options))
        return;
      source = typeof options.head === "function" ? () => options.head.call(instance.proxy) : options.head;
    } else {
      const head = this.$options.head;
      if (head) {
        source = typeof head === "function" ? () => head.call(this) : head;
      }
    }
    source && useHead(source);
  }
};

// node_modules/@unhead/vue/dist/polyfill.mjs
function polyfillAsVueUseHead(head) {
  const polyfilled = head;
  polyfilled.headTags = head.resolveTags;
  polyfilled.addEntry = head.push;
  polyfilled.addHeadObjs = head.push;
  polyfilled.addReactiveEntry = (input, options) => {
    const api = useHead(input, options);
    if (api !== void 0)
      return api.dispose;
    return () => {
    };
  };
  polyfilled.removeHeadObjs = () => {
  };
  polyfilled.updateDOM = () => {
    head.hooks.callHook("entries:updated", head);
  };
  polyfilled.unhead = head;
  return polyfilled;
}

// node_modules/@unhead/ssr/dist/index.mjs
function encodeAttribute(value) {
  return String(value).replace(/"/g, "&quot;");
}
function propsToString(props) {
  let attrs = "";
  for (const key in props) {
    if (!Object.prototype.hasOwnProperty.call(props, key)) {
      continue;
    }
    const value = props[key];
    if (value !== false && value !== null) {
      attrs += value === true ? ` ${key}` : ` ${key}="${encodeAttribute(value)}"`;
    }
  }
  return attrs;
}
function ssrRenderTags(tags, options) {
  const schema = { htmlAttrs: {}, bodyAttrs: {}, tags: { head: "", bodyClose: "", bodyOpen: "" } };
  const lineBreaks = !(options == null ? void 0 : options.omitLineBreaks) ? "\n" : "";
  for (const tag of tags) {
    if (Object.keys(tag.props).length === 0 && !tag.innerHTML && !tag.textContent) {
      continue;
    }
    if (tag.tag === "htmlAttrs" || tag.tag === "bodyAttrs") {
      Object.assign(schema[tag.tag], tag.props);
      continue;
    }
    const s = tagToString(tag);
    const tagPosition = tag.tagPosition || "head";
    schema.tags[tagPosition] += schema.tags[tagPosition] ? `${lineBreaks}${s}` : s;
  }
  return {
    headTags: schema.tags.head,
    bodyTags: schema.tags.bodyClose,
    bodyTagsOpen: schema.tags.bodyOpen,
    htmlAttrs: propsToString(schema.htmlAttrs),
    bodyAttrs: propsToString(schema.bodyAttrs)
  };
}
function escapeHtml(str) {
  return str.replace(/[&<>"'/]/g, (char) => {
    switch (char) {
      case "&":
        return "&amp;";
      case "<":
        return "&lt;";
      case ">":
        return "&gt;";
      case '"':
        return "&quot;";
      case "'":
        return "&#x27;";
      case "/":
        return "&#x2F;";
      default:
        return char;
    }
  });
}
function tagToString(tag) {
  const attrs = propsToString(tag.props);
  const openTag = `<${tag.tag}${attrs}>`;
  if (!TagsWithInnerContent.has(tag.tag))
    return SelfClosingTags.has(tag.tag) ? openTag : `${openTag}</${tag.tag}>`;
  let content = String(tag.innerHTML || "");
  if (tag.textContent)
    content = escapeHtml(String(tag.textContent));
  return SelfClosingTags.has(tag.tag) ? openTag : `${openTag}${content}</${tag.tag}>`;
}
async function renderSSRHead(head, options) {
  const beforeRenderCtx = { shouldRender: true };
  await head.hooks.callHook("ssr:beforeRender", beforeRenderCtx);
  if (!beforeRenderCtx.shouldRender) {
    return {
      headTags: "",
      bodyTags: "",
      bodyTagsOpen: "",
      htmlAttrs: "",
      bodyAttrs: ""
    };
  }
  const ctx = { tags: await head.resolveTags() };
  await head.hooks.callHook("ssr:render", ctx);
  const html = ssrRenderTags(ctx.tags, options);
  const renderCtx = { tags: ctx.tags, html };
  await head.hooks.callHook("ssr:rendered", renderCtx);
  return renderCtx.html;
}

// node_modules/@unhead/vue/dist/components.mjs
function addVNodeToHeadObj(node, obj) {
  const nodeType = !Vue3 ? node.tag : node.type;
  const type = nodeType === "html" ? "htmlAttrs" : nodeType === "body" ? "bodyAttrs" : nodeType;
  if (typeof type !== "string" || !(type in obj))
    return;
  const nodeData = !Vue3 ? node.data : node;
  const props = (!Vue3 ? nodeData.attrs : node.props) || {};
  if (!Vue3) {
    if (nodeData.staticClass)
      props.class = nodeData.staticClass;
    if (nodeData.staticStyle)
      props.style = Object.entries(nodeData.staticStyle).map(([key, value]) => `${key}:${value}`).join(";");
  }
  if (node.children) {
    const childrenAttr = !Vue3 ? "text" : "children";
    props.children = Array.isArray(node.children) ? node.children[0][childrenAttr] : node[childrenAttr];
  }
  if (Array.isArray(obj[type]))
    obj[type].push(props);
  else if (type === "title")
    obj.title = props.children;
  else
    obj[type] = props;
}
function vnodesToHeadObj(nodes) {
  const obj = {
    title: void 0,
    htmlAttrs: void 0,
    bodyAttrs: void 0,
    base: void 0,
    meta: [],
    link: [],
    style: [],
    script: [],
    noscript: []
  };
  for (const node of nodes) {
    if (typeof node.type === "symbol" && Array.isArray(node.children)) {
      for (const childNode of node.children)
        addVNodeToHeadObj(childNode, obj);
    } else {
      addVNodeToHeadObj(node, obj);
    }
  }
  return obj;
}
var Head = defineComponent({
  name: "Head",
  setup(_, { slots }) {
    const head = injectHead();
    const obj = ref({});
    const entry = head.push(obj);
    onBeforeUnmount(() => {
      entry.dispose();
    });
    return () => {
      watchEffect(() => {
        if (!slots.default)
          return;
        entry.patch(vnodesToHeadObj(slots.default()));
      });
      return null;
    };
  }
});

// node_modules/@vueuse/head/dist/index.mjs
function createHead3(initHeadObject, options) {
  const unhead = createHead2(options || {});
  const legacyHead = polyfillAsVueUseHead(unhead);
  if (initHeadObject)
    legacyHead.push(initHeadObject);
  return legacyHead;
}
var HeadVuePlugin = Vue2ProvideUnheadPlugin;
var renderHeadToString = (head) => renderSSRHead(head.unhead);
export {
  Head,
  HeadVuePlugin,
  Vue2ProvideUnheadPlugin,
  VueHeadMixin,
  createHead3 as createHead,
  createHeadCore,
  injectHead,
  renderHeadToString,
  unheadVueComposablesImports,
  useHead,
  useHeadSafe,
  useSeoMeta,
  useServerHead,
  useServerHeadSafe,
  useServerSeoMeta
};
//# sourceMappingURL=@vueuse_head.js.map
